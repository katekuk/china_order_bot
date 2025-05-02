# Телеграм-бот для помощи с заказами из китайских маркетплейсов
import aiohttp
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
import asyncio

# Вставь сюда свой токен Telegram-бота
TOKEN = os.getenv("TOKEN") or "ВАШ_ТОКЕН_ЗДЕСЬ"

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Основное меню
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍭 Как заказать")],
        [KeyboardButton(text="🧮 Расчет стоимости")],
        [KeyboardButton(text="🚚 Доставка")],
        [KeyboardButton(text="🔍 Поиск на маркетплейсах")],
        [KeyboardButton(text="📈 Курс юаня")]
    ], resize_keyboard=True
)

async def get_cny_rate():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return round(data["Valute"]["CNY"]["Value"], 2)
    except Exception as e:
        return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Я помогу вам с заказами из Китая 🇨🇳. Выберите интересующий пункт меню:", reply_markup=main_kb)

@dp.message(F.text == "🍭 Как заказать")
async def how_to_order(message: types.Message):
    text = (
        "✉️ Для оформления заказа пришлите:"
            "- Ссылку на товар с китайского маркетплейса"
            "- Скриншот с выбранной характеристикой товара (размер, цвет и т.д.)"
        "Пример ссылки: https://item.taobao.com/item.htm?id=123456789"
    )
    await message.answer(text)

@dp.message(F.text == "🧮 Расчет стоимости")
async def calc_menu(message: types.Message):
    buttons = [
        [KeyboardButton(text="✅ Рассчитать"), KeyboardButton(text="🔢 Формула расчета")],
        [KeyboardButton(text="🔙 Назад к меню")]
    ]
    await message.answer("Выберите действие:", reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

@dp.message(F.text == "✅ Рассчитать")
async def start_calculation(message: types.Message):
    await message.answer("📅 Введите стоимость товара в юанях:")
    dp.message.register(handle_price_input)

async def handle_price_input(message: types.Message):
    try:
        cny = float(message.text)
        rate = await get_cny_rate()
        total = round(cny * rate * 1.15, 2)
        await message.answer(f"✉️ Стоимость в рублях: <b>{total}</b> ₽ (по курсу {rate} + 15%)")
    except ValueError:
        await message.answer("❌ Пожалуйста, введите число (стоимость в юанях).")

@dp.message(F.text == "🔢 Формула расчета")
async def calc_formula(message: types.Message):
    text = (
        "🔢 <b>Формула расчета:</b>\n"
        "стоимость (юани) × курс × 1.15\n\n"
        "В 15% включена работа китайской стороны: проверка товара, хранение на складе, оформление и сопровождение."
    )
    await message.answer(text)

@dp.message(F.text == "🚚 Доставка")
async def delivery_menu(message: types.Message):
    buttons = [
        [KeyboardButton(text="💸 Сколько стоит доставка"), KeyboardButton(text="⏱️ Сроки доставки")],
        [KeyboardButton(text="💾 Примерный вес товаров"), KeyboardButton(text="🔙 Назад к меню")]
    ]
    await message.answer("Выберите интересующий пункт:", reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

@dp.message(F.text == "💸 Сколько стоит доставка")
async def delivery_cost(message: types.Message):
    await message.answer("1 кг = 690 руб. Оплата по фактическому весу после прибытия в Хабаровск. Взвешивается товар с упаковкой.")

@dp.message(F.text == "⏱️ Сроки доставки")
async def delivery_time(message: types.Message):
    await message.answer("Средний срок: 3-4 недели. Возможны задержки из-за таможни, но мы стараемся максимально ускорить процесс.")

@dp.message(F.text == "💾 Примерный вес товаров")
async def item_weight(message: types.Message):
    await message.answer("Футболка – 0.5 кг\nДжинсы – 1.5-3 кг\nОбувь – 1.5-3 кг\nМаленькая сумка – 0.8-1 кг\nБольшая сумка – 1-2.5 кг")

@dp.message(F.text == "🔍 Поиск на маркетплейсах")
async def marketplaces_menu(message: types.Message):
    buttons = [
        [KeyboardButton(text="📊 Китайские маркетплейсы")],
        [KeyboardButton(text="💾 Как скачать и зарегистрироваться")],
        [KeyboardButton(text="📽️ Инструкции по маркетплейсам")],
        [KeyboardButton(text="🔙 Назад к меню")]
    ]
    await message.answer("Выберите пункт:", reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

@dp.message(F.text == "📊 Китайские маркетплейсы")
async def china_marketplaces(message: types.Message):
    await message.answer("ТаоБао – массовый маркет\nPoizon – оригинальные бренды\n1688 – опт/фабрики\n95 – люкс ресейл\nСкачайте приложение для доступа.")

@dp.message(F.text == "💾 Как скачать и зарегистрироваться")
async def how_to_register(message: types.Message):
    await message.answer("Скачайте приложения с App Store / Google Play. Рекомендуется регистрация через Alipay – безопасно и стабильно.")

@dp.message(F.text == "📽️ Инструкции по маркетплейсам")
async def video_guides(message: types.Message):
    await message.answer("Видео-инструкции доступны по запросу.\nТаоБао, Poizon, 1688, 95 – напишите, и мы пришлём видео.")

@dp.message(F.text == "📈 Курс юаня")
async def show_rate(message: types.Message):
    rate = await get_cny_rate()
    if rate:
        await message.answer(f"📈 Сегодняшний курс юаня: {rate} ₽.\nФинальный курс фиксируется в момент заказа.")
    else:
        await message.answer("❌ Не удалось получить курс юаня. Попробуйте позже.")

@dp.message(F.text == "🔙 Назад к меню")
async def back_to_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_kb)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
