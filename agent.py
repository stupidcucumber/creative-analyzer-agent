import asyncio
import re
import os
import pathlib
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.text_decorations import markdown_decoration as md
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


MAX_MESSAGE_LENGTH = 4000

def split_text(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Splits a string into chunks without breaking lines if possible."""
    if len(text) <= max_length:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        
        # Find the best place to split (newline preferred)
        split_at = text.rfind('\n', 0, max_length)
        
        # If no newline, look for a space
        if split_at == -1:
            split_at = text.rfind(' ', 0, max_length)
            
        # If no space, hard split at max_length
        if split_at == -1:
            split_at = max_length

        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()
        
    return chunks


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
        for part in split_text(answer):
            part = md.quote(part)
            await message.answer(part, parse_mode="MarkdownV2")
        
    except Exception as e:
        await message.answer(f"Сталася помилка: {str(e)}")
        

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())