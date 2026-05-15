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
Ти — експерт із Data Engineering та SQL Optimization. Твоє завдання: згенерувати точний та ефективний SQL-запит до бази даних SQLite на основі текстового запиту маркетолога.

### Schema Context
Ось опис таблиць та колонок у базі даних (основна таблиця `marketing`):
{column_description}

### Constraints & Business Logic
1. ВИКОРИСТОВУЙ ТІЛЬКИ СИНТАКСИС SQLite! Ніяких `INTERVAL`, `DATEADD` чи `CURRENT_DATE`.
2. Обов'язкова фільтрація дат: Завжди додавай умову `date_published IS NOT NULL`, якщо в запиті є хоч якась прив'язка до часу чи дат. 
3. Обов'язковий вивід дати: Якщо запит пов'язаний з часом, результуючий `SELECT` повинен включати колонку `date_published` (або агрегацію по ній).
4. Використовуй CTE (Common Table Expressions) `WITH ... AS (...)` для складних запитів (порівняння періодів, пошук нових сутностей), щоб запит був читабельним.
5. Повертай ТІЛЬКИ валідний SQL-код без маркдаун-форматування (або строго в блоці ```sql), без додаткових пояснень.
6. Результат виконання SQL запиту буде аналізувати ще один агент, тож додай в запит якомога більше колонок. В запиті обов'язково має бути присутня `date_published`, якщо треба агрегуй як максимальна дата в групі.

### Date & Time Handling in SQLite
Для роботи з часом використовуй виключно функцію `date('now', '<modifier>')`. 
Шпаргалка модифікаторів для цього завдання:
- "сьогодні" -> `date('now')`
- "останній тиждень" / "останні 7 днів" -> `>= date('now', '-7 days')`
- "попередній тиждень" (для порівняння) -> `BETWEEN date('now', '-14 days') AND date('now', '-7 days')`
- "останні 2 тижні" -> `>= date('now', '-14 days')`
- "попередні 2 тижні до того" -> `BETWEEN date('now', '-28 days') AND date('now', '-14 days')`
- "цього місяця" -> `>= date('now', 'start of month')`
- "минулого місяця" -> `BETWEEN date('now', 'start of month', '-1 month') AND date('now', 'start of month')`

### Task Cases & SQL Patterns
Застосовуй ці підходи для відповідних типів питань:
- **Top Hooks (Найкращі хуки за час X):** 
  Фільтр `date_published >= ...` + `ORDER BY reach DESC`.
- **New Hooks (Нові хуки за час X, яких не було раніше):** 
  Використовуй підзапит. Знайти хуки, де `date_published >= [Current Period]`, і `hook NOT IN (SELECT hook FROM marketing WHERE date_published < [Current Period])`.
- **Trends (Порівняння поточного періоду з попереднім):** 
  Використовуй 2 CTE: `current_period` та `previous_period`. Зроби `FULL OUTER JOIN` або `LEFT JOIN` за ключовим атрибутом (наприклад, hook або format) і порахуй різницю (`reach_current - reach_previous`) або зміну у відсотках.
- **Ideal Creative (Ідеальний креатив):** 
  Використовуй агрегацію (наприклад, `AVG(reach)`) для різних атрибутів (формат, тривалість, хук). Знайди комбінацію атрибутів, яка історично дає найвищий середній `reach`. Згрупуй за цими атрибутами `GROUP BY ... ORDER BY AVG(reach) DESC LIMIT 1`.
- **Best Formats (Найкращі формати за час X):**
  Згрупуй за форматом (`GROUP BY format`), порахуй `AVG(reach)` або `SUM(reach)`, додай фільтр часу `WHERE date_published >= ...`.

### Input Question
Користувач запитує: "{question}"

{error_context}""")
		
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

		print("SQL Query: ", sql_query)
		
		try:

			if "DELETE" in sql_query or "ALTER" in sql_query or "UPDATE" in sql_query or "INSERT" in sql_query:
				raise sqlite3.Error("You can't use DELETE, ALTER, UPDATE, or INSERT.")

			with sqlite3.connect(self.database_path) as conn:
				conn.row_factory = sqlite3.Row
				cursor = conn.cursor()
				cursor.execute(sql_query)
				rows = cursor.fetchall()
				
				result_list = [dict(row) for row in rows]
				
		except sqlite3.Error as e:
			return {"error": str(e), "sql_result": None}
		
		print("Result: ", str(result_list))
		
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
