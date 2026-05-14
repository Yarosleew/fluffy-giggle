import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
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


# Визначаємо структуру для CallbackData магазину
class BuyCallback(CallbackData, prefix="buy"):
    item: str


# --- КЛАВІАТУРИ ---

# Головне меню (Reply)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привіт 👋"), KeyboardButton(text="Як справи? 😊")],
        [KeyboardButton(text="Анекдот 🤣"), KeyboardButton(text="Магазин 🛒")],
        [KeyboardButton(text="Цікавий факт про Dota 2 🎮")],  # Нова кнопка
        [KeyboardButton(text="Меню Inline 🔘")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть пункт меню..."
)

# Кнопка для гравців (Inline)
dota_players_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Найвідоміші гравці 🏆", callback_data="top_players")]
    ]
)

# Вбудовані кнопки (Inline)
inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Погода ☁️", callback_data="weather_info"),
            InlineKeyboardButton(text="Жарт 🎭", callback_data="joke_inline")
        ],
        [
            InlineKeyboardButton(text="Сайт Python 🐍", url="https://www.python.org"),
            InlineKeyboardButton(text="Закрити ❌", callback_data="close_menu")
        ]
    ]
)

# Клавіатура магазину
shop_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍎 Яблуко", callback_data=BuyCallback(item="apple").pack())],
        [InlineKeyboardButton(text="🍌 Банан", callback_data=BuyCallback(item="banana").pack())],
        [InlineKeyboardButton(text="🍇 Виноград", callback_data=BuyCallback(item="grape").pack())],
    ]
)


# --- ОБРОБНИКИ КОМАНД ---

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Вітаю, {message.from_user.first_name}! 🤖\nЯ об'єднаний бот-помічник.",
        reply_markup=main_menu
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Використовуй кнопки меню! Команда /start оновить інтерфейс.")


# --- ОБРОБКА ТЕКСТУ ---

@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.lower()

    if text == "привіт 👋":
        await message.answer("Привіт! ✨")
    elif text == "як справи? 😊":
        await message.answer("Все чудово! Працюю як годинник ⚙️")
    elif text == "анекдот 🤣":
        await message.answer(
            "— Куме, а що таке 'хмарні технології'?\n— Це коли твої гроші випаровуються швидше, ніж ти встигаєш їх заробити! ☁️")

    # Новий функціонал про Dota 2
    elif text == "цікавий факт про dota 2 🎮":
        fact_text = (
            "🎮 **Dota 2** — одна з найпопулярніших кіберспортивних дисциплін, "
            "що вийшла у 2013 році та славиться понад 120 унікальними героями, "
            "величезними призовими фондами (що перевищували $40 млн на The International)."
        )
        await message.answer(fact_text, reply_markup=dota_players_keyboard, parse_mode="Markdown")

    elif text == "магазин 🛒":
        await message.answer("Оберіть товар у нашому маркеті:", reply_markup=shop_keyboard)
    elif text == "меню inline 🔘":
        await message.answer("Додаткові функції:", reply_markup=inline_menu)
    else:
        await message.answer("Будь ласка, оберіть варіант з меню нижче 👇")


# --- ОБРОБКА CALLBACK ---

@dp.callback_query(F.data == "top_players")
async def callback_players(callback: CallbackQuery):
    players_info = (
        "🌟 **Легендарні гравці:**\n\n"
        "1. **Йохан «N0tail» Сундштайн (Danmark):** Один із найуспішніших гравців в історії, "
        "капітан OG, який виграв два The International (2018, 2019).\n\n"
        "2. **Амер «Miracle-» Аль-Баркаві (Jordan/Poland):** Відомий своїми неймовірними "
        "механічними навичками та грою на центральній лінії (mid) та кері (carry).\n\n"
        "3. **Данило «Dendi» Ішутін (Ukraine):** Легендарний мідер, символ перших років Dota 2 "
        "та переможець першого The International (2011) у складі Natus Vincere."
    )
    await callback.message.answer(players_info, parse_mode="Markdown")
    await callback.answer()


@dp.callback_query(BuyCallback.filter())
async def handle_buy_callback(callback: CallbackQuery, callback_data: BuyCallback):
    item_name = callback_data.item
    translations = {"apple": "Яблуко", "banana": "Банан", "grape": "Виноград"}
    await callback.message.answer(f"Ти обрав: {translations.get(item_name, item_name)} ✅")
    await callback.answer()


@dp.callback_query(F.data == "weather_info")
async def callback_weather(callback: CallbackQuery):
    await callback.message.answer("На вулиці чудова погода для кодингу! ☀️")
    await callback.answer()


@dp.callback_query(F.data == "joke_inline")
async def callback_joke(callback: CallbackQuery):
    await callback.message.answer("Чому програмісти не люблять природу? Там забагато багів! 🐛")
    await callback.answer()


@dp.callback_query(F.data == "close_menu")
async def callback_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Меню закрито")


# --- ЗАПУСК ---

async def main():
    print("Бот запущений та готовий до роботи...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений користувачем")