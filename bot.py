import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CallbackQuery
)

# --- НАЛАШТУВАННЯ ---
API_TOKEN = "8742759318:AAFPb8YA4nosD5GsXcsjZGvo76SvY6b9ZHc"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- КЛАВІАТУРИ ---

# Головне меню (Reply)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привіт 👋"), KeyboardButton(text="Як справи? 😊")],
        [KeyboardButton(text="Анекдот 🤣"), KeyboardButton(text="Меню Inline 🔘")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть пункт меню..."
)

# Вбудовані кнопки (Inline)
inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Погода ☁️", callback_data="weather_info"), # НОВА КНОПКА
            InlineKeyboardButton(text="Жарт 🎭", callback_data="joke_inline")
        ],
        [
            InlineKeyboardButton(text="Сайт Python 🐍", url="https://www.python.org"),
            InlineKeyboardButton(text="Закрити ❌", callback_data="close_menu")
        ]
    ]
)

# --- ОБРОБНИКИ КОМАНД ---

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Вітаю, {message.from_user.first_name}! 🤖\nЯ готовий до роботи.",
        reply_markup=main_menu
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Використовуй меню для керування ботом! Команда /start оновить кнопки.")

# --- ОБРОБКА ТЕКСТУ ---

@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.lower()

    if text == "привіт 👋":
        await message.answer("Привіт! ✨")
    elif text == "як справи? 😊":
        await message.answer("Все чудово! ⚙️")
    elif text == "анекдот 🤣":
        await message.answer("Програміст іде спати і ставить на тумбочку дві склянки. Одну з водою — якщо захоче пити, іншу порожню — якщо не захоче. 😂")
    elif text == "меню inline 🔘":
        await message.answer("Додаткові функції:", reply_markup=inline_menu)
    else:
        await message.answer("Натисни кнопку в меню 👇")

# --- ОБРОБКА CALLBACK (INLINE КНОПКИ) ---

# НОВИЙ ОБРОБНИК ДЛЯ ПОГОДИ
@dp.callback_query(F.data == "weather_info")
async def callback_weather(callback: CallbackQuery):
    await callback.message.answer("Я не синоптик 😅")
    await callback.answer() # Прибирає завантаження на кнопці

@dp.callback_query(F.data == "joke_inline")
async def callback_joke(callback: CallbackQuery):
    await callback.message.answer("Чому програмісти не люблять природу? Там забагато багів! 🐛")
    await callback.answer()

@dp.callback_query(F.data == "close_menu")
async def callback_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

# --- ЗАПУСК ---

async def main():
    print("Бот запущений...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений")