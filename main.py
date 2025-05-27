import logging
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = Path("prompt.txt").read_text()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

user_sessions = {}

@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer("Привет. Я Вера. Я здесь, чтобы быть рядом. Ты можешь быть анонимным, если хочешь. Расскажи, что у тебя сейчас на сердце 💜")
    user_sessions[message.from_user.id] = []

@dp.message_handler()
async def chat(message: Message):
    user_id = message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    history = user_sessions[user_id]

    history.append({"role": "user", "content": message.text})

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history
            ],
            temperature=0.8,
        )

        reply = response.choices[0].message.content
        await message.answer(reply)
        history.append({"role": "assistant", "content": reply})

    except Exception as e:
        await message.answer("Прости, что-то пошло не так. Попробуй ещё раз чуть позже 🙏")
        logging.exception("OpenAI API error")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
