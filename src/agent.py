import pathlib
import sqlite3
from src.characteristics_types import DatabaseEntry
from typing import TypedDict, Annotated, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import BaseChatModel
from langchain.messages import HumanMessage
from langgraph.graph import StateGraph, END


class AgentState(TypedDict, total=False):
	messages: Annotated[list[HumanMessage], "Список повідомлень"]
	generated_sql: Optional[str]
	sql_result: Optional[str] 
	final_answer: Optional[str]
	error: Optional[str]
	retry_count: int


class ChatAgent:
	def __init__(self, llm: BaseChatModel, database_path: pathlib.Path, max_retries: int = 3) -> None:
		self.llm = llm
		self.database_path = database_path
		self.max_retries = max_retries

		workflow = StateGraph(AgentState)
		
		workflow.add_node("generate_sql", self.sql_generator_node)
		workflow.add_node("execute_sql", self.execute_sql_node)
		workflow.add_node("formulate_answer", self.answer_node)
		
		workflow.set_entry_point("generate_sql")
		workflow.add_edge("generate_sql", "execute_sql")
		
		workflow.add_conditional_edges(
			"execute_sql",
			self.should_continue,
			{
				"retry": "generate_sql",
				"continue": "formulate_answer"
			}
		)
		
		workflow.add_edge("formulate_answer", END)

		self.app = workflow.compile()

	def should_continue(self, state: AgentState) -> str:
		"""
		Determines if the agent should retry SQL generation or move to answering.
		"""
		if state.get("error") and state.get("retry_count", 0) < self.max_retries:
			return "retry"
		return "continue"

	def sql_generator_node(self, state: AgentState) -> dict:
		print("\t\tGenerating SQL code.")

		error_context = ""
		if state.get("error"):
			error_context = f"\nПОПЕРЕДНЯ ПОМИЛКА: {state['error']}\nБудь ласка, виправ цей запит."

		prompt = ChatPromptTemplate.from_template("""
		Ти — експерт з аналізу маркетингових даних. 
											
		Твоя база даних SQLite має таблицю `marketing` з полями:
		{columns}
		
		Завдання: Напиши SQL запит який би міг допомогти відповісти аналітикам на питання: {question}
		
		{error_context}
		
		Поверни ТІЛЬКИ чистий SQL код без Markdown блоків.
		""")
		
		question = state["messages"][-1].content
		response = self.llm.invoke(prompt.format(
			columns="(" + "), (".join(DatabaseEntry.database_columns()) + ")",
			question=question, 
			error_context=error_context
		))
		
		sql = response.content.replace("```sql", "").replace("```", "").strip()
		
		return {"generated_sql": sql, "retry_count": state.get("retry_count", 0) + 1}

	def execute_sql_node(self, state: AgentState) -> dict:
		print("\t\tExecuting SQL code.")
		sql_query = state.get("generated_sql")
		
		try:
			with sqlite3.connect(self.database_path) as conn:
				conn.row_factory = sqlite3.Row
				cursor = conn.cursor()
				cursor.execute(sql_query)
				rows = cursor.fetchall()
				
				result_list = [dict(row) for row in rows]
				
		except sqlite3.Error as e:
			return {"error": str(e), "sql_result": None}
		
		return {"sql_result": str(result_list), "error": None}

	def answer_node(self, state: AgentState) -> dict:
		print("\t\tGenerating an answer.")

		if state.get("error"):
			return {"final_answer": f"Вибачте, я не зміг виконати запит до бази даних після кількох спроб. Помилка: {state['error']}"}

		prompt = ChatPromptTemplate.from_template("""
			Ти професійний маркетинговий аналітик. 
			На основі SQL результату: 
				{sql_result}
			Сформулюй коротку та професійну відповідь на питання: 
				{question}
			"""
		)
		
		question = state["messages"][-1].content
		response = self.llm.invoke(prompt.format(
			sql_result=state["sql_result"],
			question=question
		))
		
		return {"final_answer": response.content}
