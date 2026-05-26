import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

user_messages = {}


def get_user_history(user_id: int):
    if user_id not in user_messages:
        user_messages[user_id] = [
            {
                "role": "system",
                "content": "Ти корисний AI-помічник українською мовою. Відповідай зрозуміло, практично і по суті."
            }
        ]
    return user_messages[user_id]


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "🤖 Вітаю! Я AI Assistant на базі DeepSeek.\n\n"
        "Можу допомогти з:\n"
        "• навчанням\n"
        "• програмуванням\n"
        "• перекладами\n"
        "• текстами\n"
        "• Cisco / MikroTik / мережами\n"
        "• AI та кібербезпекою\n\n"
        "Просто напишіть своє питання 👇"
    )


@dp.message(Command("reset"))
async def reset(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_messages:
        del user_messages[user_id]

    await message.answer("✅ Контекст діалогу очищено. Можемо почати спочатку.")


@dp.message()
async def ai_reply(message: types.Message):
    user_id = message.from_user.id

    if message.text is None:
        if message.voice:
            await message.answer(
                "🎙️ Я отримав голосове повідомлення, але поки ще не вмію його розпізнавати.\n\n"
                "Будь ласка, надішли текстом."
            )
            return

        if message.photo:
            await message.answer(
                "🖼️ Я отримав фото, але поки ще не вмію аналізувати зображення.\n\n"
                "Опиши фото текстом — і я допоможу."
            )
            return

        await message.answer(
            "⚠️ Поки що я працюю тільки з текстовими повідомленнями."
        )
        return

    history = get_user_history(user_id)

    await bot.send_chat_action(message.chat.id, "typing")

    history.append({
        "role": "user",
        "content": message.text
    })

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=history
        )

        answer = response.choices[0].message.content

        history.append({
            "role": "assistant",
            "content": answer
        })

        await message.answer(answer)

    except Exception as e:
        print(f"Помилка: {e}")
        await message.answer(
            "❌ Сталася помилка під час обробки запиту. Спробуй ще раз."
        )

    answer = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": answer
    })

    await message.answer(answer)


async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())