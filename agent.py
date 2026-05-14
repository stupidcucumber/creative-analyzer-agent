import asyncio
import os
import pathlib
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from langchain_core.messages import HumanMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from src.agent import ChatAgent, AgentState
from src.analyzer_model import GeminiModelType
from langchain_core.runnables import RunnableConfig

from dotenv import load_dotenv

load_dotenv()


bot = Bot(token=os.getenv("TELEGRAM_BOT_API_TOKEN", ""))
dp = Dispatcher()
chat_agent = ChatAgent(
    llm=ChatGoogleGenerativeAI(model=str(GeminiModelType.GEMINI_2_5_FLASH)), 
    database_path=pathlib.Path("data.sqlite3")
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я AI-аналітик маркетингових креативів. \n"
        "Запитай мене про найкращі хуки, формати або тренди тижня."
    )


@dp.message()
async def handle_message(message: types.Message):
    print("Received a question: ", message.text)
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    print("Start execution.")
    try:
        config = RunnableConfig(configurable={"thread_id": str(message.chat.id)})
        state = AgentState(messages=[HumanMessage(content=message.text)])
        
        print("\tInvoking an agent.")
        result = chat_agent.app.invoke(state, config)
        
        print(f"\tExtracting final answer: {result["final_answer"]}")
        answer = result["final_answer"]

        print("\tSending answer to the user.")
        await message.answer(answer)
        
    except Exception as e:
        await message.answer(f"Сталася помилка: {str(e)}")
        

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())