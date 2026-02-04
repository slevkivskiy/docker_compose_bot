import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАЛАШТУВАННЯ ---
TOKEN = "8432767136:AAESi8lIgC8QSG5E0qZGWKC_mn54JG8TFqU"  # <--- НЕ ЗАБУДЬ ВСТАВИТИ ТОКЕН!

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- 1. ГОЛОВНЕ МЕНЮ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Кнопка 1: Дія всередині чату (Callback)
    b1 = InlineKeyboardButton(text="🎲 Кинути кубик", callback_data="throw_dice")

    # Кнопка 2: Спливаюче вікно (Callback)
    b2 = InlineKeyboardButton(text="👤 Хто я?", callback_data="show_info")

    # Кнопка 3: Посилання (URL) - ТВОЄ ЗАВДАННЯ
    # Зверни увагу: тут немає callback_data, тут є url
    b3 = InlineKeyboardButton(text="Мій GitHub 🐙", url="https://github.com/slevkivskiy/bash_automation_tools")

    # Збираємо клавіатуру
    # Перший ряд: Кубик і Інфо
    # Другий ряд: Гітхаб (на всю ширину)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [b1, b2],
        [b3]
    ])

    await message.answer("Привіт! Це твоє портфоліо-меню:", reply_markup=keyboard)


# --- 2. ОБРОБКА КЛІКІВ ---

# Ловимо кубик
@dp.callback_query(F.data == "throw_dice")
async def process_dice(callback: types.CallbackQuery):
    await callback.answer()  # Прибираємо годинничок
    await callback.message.answer_dice(emoji="🎲")


# Ловимо інфо (з alert=True)
@dp.callback_query(F.data == "show_info")
async def process_info(callback: types.CallbackQuery):
    await callback.answer("Я бот, написаний на Python + aiogram!", show_alert=True)


# ПРИМІТКА: Хендлер для кнопки GitHub писати НЕ ТРЕБА.
# Телеграм сам перекине юзера в браузер.

# --- ЗАПУСК ---
async def main():
    print("Бот з GitHub-кнопкою запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений.")