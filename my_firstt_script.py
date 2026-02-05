import asyncio
import logging
import sys
import os # Щоб читати змінні (токен)

# Імпортуємо Redis (асинхронну версію, бо у нас aiogram)
import redis.asyncio as redis

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Дістаємо токен з "сейфа"
TOKEN = os.getenv("BOT_TOKEN")

# Підключаємось до Redis
# host="redis_db" — ЦЕ ВАЖЛИВО! Це ім'я сервісу з docker-compose.yml
# Докер сам підставить правильний IP.
r = redis.Redis(host='redis_db', port=6379, decode_responses=True)

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # 1. Збільшуємо лічильник в базі даних на +1
    # 'visits' — це ключ (назва комірки в пам'яті Redis)
    visits = await r.incr("visits")

    # 2. Формуємо відповідь
    text = f"Hello, {html.bold(message.from_user.full_name)}! 👋\n" \
           f"Ти запустив цей бот вже <b>{visits}</b> разів.\n" \
           f"Ця цифра живе в базі даних Redis!"

    # Створюємо кнопку
    b1 = InlineKeyboardButton(text="🎲 pipipupu", callback_data="throw_dice")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[b1]])

    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == 'throw_dice')
async def process_callback_button1(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer_dice(emoji="🎲")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())