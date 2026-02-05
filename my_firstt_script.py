import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# os.getenv шукає змінну з такою назвою в системі
TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    b1 = InlineKeyboardButton(text="🎲 pipipupu", callback_data="throw_dice")

    b2 = InlineKeyboardButton(text="👤 Хто я?", callback_data="show_info")

    b3 = InlineKeyboardButton(text="Мій GitHub 🐙", url="https://github.com/slevkivskiy")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [b1, b2],
        [b3]
    ])

    await message.answer("Привіт! Це твоє портфоліо-меню:", reply_markup=keyboard)

@dp.callback_query(F.data == "throw_dice")
async def process_dice(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_dice(emoji="🎲")

@dp.callback_query(F.data == "show_info")
async def process_info(callback: types.CallbackQuery):
    await callback.answer("Bot deployed via CD!", show_alert=True)

# --- ЗАПУСК ---
async def main():
    print("Бот з GitHub-кнопкою запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений.")