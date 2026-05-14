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

		prompt = ChatPromptTemplate.from_template("""### Role
Ти — експерт із Data Engineering та SQL Optimization. Твоє завдання: згенерувати точний та ефективний SQL-запит на основі текстового опису маркетингової задачі.

### Schema Context
Ось опис таблиць та колонок у базі даних з таблицею `marketing`:
{column_description}

### Constraints & Business Logic
При генерації запиту суворо дотримуйся наступних правил:
1. **Timeframe:** Якщо запит стосується "останнього тижня", використовуй `CURRENT_DATE - INTERVAL '7 days'`. Якщо "місяць" — `DATE_TRUNC('month', CURRENT_DATE)`.
2. **Hook Uniqueness:** Для пошуку "нових хуків" використовуй `NOT EXISTS` або `LEFT JOIN ... WHERE ... IS NULL`, порівнюючи поточний період з усією історією до цього.
3. **Metrics:** Reach — це сума (`SUM`), але якщо запит про формати — використовуй `AVG(reach)` для коректного порівняння ефективності різних типів контенту.
4. **Performance:** Завжди додавай `LIMIT 100`, якщо не вказано інше, щоб не перевантажувати систему.
5. **Format:** Повертай **ТІЛЬКИ** чистий SQL-код у блоку markdown. Без вступних фраз чи пояснень.

### Task Cases Logic
- **Top Hooks:** Фільтр за датою завантаження (`upload_date`) + `ORDER BY reach DESC`.
- **New Hooks:** Порівняння множини хуків за останні 7 днів із множиною за попередній період.
- **Ideal Creative:** Агрегація за всіма ключовими атрибутами (format, color, length, hook_type) з розрахунком середнього reach.
- **Trends:** Використання `CASE WHEN` або двох `CTE`, щоб вирахувати Delta (%) між двома часовими проміжками.

### Input Question
Користувач запитує: "{question}"
											
{error_context}
		""")
		
		question = state["messages"][-1].content
		response = self.llm.invoke(prompt.format(
			question=question, 
			column_description=DatabaseEntry.generate_prompt(),
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

		prompt = ChatPromptTemplate.from_template("""### Role
Ти — провідний Marketing Data Analyst в AI-агентстві. Твоя спеціалізація — перетворення сирих SQL-даних у стратегічні інсайти для медіабаїнгу та контент-команд.

### Context
Тобі надано результати SQL-запиту, що містять метрики ефективності рекламних креативів (Reach, CTR, Hooks, Formats тощо).
- **SQL Result:** {sql_result}
- **Database Schema & Metadata:** {column_description}

### Task
Сформулюй коротку, професійну та аналітично обґрунтовану відповідь на питання: "{question}".

### Analysis Guidelines
Залежно від типу питання, використовуй наступну логіку:

1. **Топ хуки (за 7 днів):** Визнач креативи, завантажені за останні 168 годин. Відсортуй їх за `reach` та виділи конкретні гачки (hooks), які забезпечили максимальне охоплення.
2. **Нові хуки (Incremental Innovation):** Знайди унікальні значення в колонці hooks, які присутні в останніх завантаженнях, але відсутні в історичних даних. Оціни їхній "перший політ" (initial performance).
3. **Ідеальний креатив (Synthesis):** Проаналізуй статистичну кореляцію між атрибутами (колір, формат, тривалість, CTA) та високим `reach`. Сформуй ТЗ на основі "переможних" комбінацій.
4. **Формати (Efficiency):** Порівняй агреговані дані: Video vs Image, Aspect Ratios (9:16 vs 1:1). Вкажи не просто "хто краще", а на скільки % різниться медіанний reach.
5. **Тренди (Dynamic Change):** Порівняй метрики поточного двотижневого періоду з попереднім. Виділи аномалії: що "вигорає", а що стрімко набирає популярність.

### Custom Capabilities (Added Values):
6. **Аналіз "Втомленості" (Creative Fatigue):** Визнач хуки, чий reach або CTR почав динамічно падати після піку. Дай рекомендацію щодо ротації.
7. **Кореляція "Візуал-Текст":** Оціни, які текстові заголовки найкраще працюють з конкретними візуальними форматами (наприклад, чи правда, що 9:16 потребує коротших хуків).

### Output Requirements
- **Стиль:** Лаконічний, без води, мова цифр та гіпотез.
- **Структура:** Коротка теза -> Ключові цифри/факти -> Рекомендація.
- **Обмеження:** Якщо даних недостатньо для впевненого висновку, вкажи на це прямо.
- **Креативність:** Якщо просять сформувати креатив, то наповни його конкретним прикладом хуку/логіки, описом сцен і т.д, як би він реально виглядав.
"""
		)
		
		question = state["messages"][-1].content
		response = self.llm.invoke(prompt.format(
			sql_result=state["sql_result"],
			column_description=DatabaseEntry.generate_prompt(),
			question=question
		))
		
		return {"final_answer": response.content}
