
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
import openai

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

SYSTEM_PROMPT = Path("prompt.txt").read_text()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_text = "Пользователь только что нажал /start. Поздоровайся, представься, пригласи к диалогу, подчеркни анонимность."
    reply = await generate_reply(user_text)
    await message.answer(reply)

@dp.message_handler()
async def message_handler(message: types.Message):
    reply = await generate_reply(message.text)
    await message.answer(reply)

async def generate_reply(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return "Прости, что-то пошло не так... Попробуй ещё раз позже 🙏"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
