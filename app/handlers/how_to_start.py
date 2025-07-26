from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

router = Router()

@router.message(F.text == "🚀 Как начать")
async def how_to_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🆕 Новый клиент")],
            [KeyboardButton(text="👤 Действующий клиент")],
            [KeyboardButton(text="🔙 В меню")],
        ],
        resize_keyboard=True
    )
    await message.answer("Выбери подходящий вариант:", reply_markup=kb)

@router.message(F.text == "🆕 Новый клиент")
async def new_client_handler(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏦 ВТБ"), KeyboardButton(text="🏦 Альфа")],
            [KeyboardButton(text="🔙 В меню")],
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Выбери банк, чтобы посмотреть условия и перейти по реферальной ссылке:",
        reply_markup=kb
    )

@router.message(F.text == "🏦 ВТБ")
async def vtb_info(message: Message):
    await message.answer(
        "🍒 <b>Условия по ВТБ:</b>\n"
        "✅ Бесплатное обслуживание\n"
        "✅ Кэшбэк 5%\n\n"
        "👉 <a href='https://example.com/vtb-ref-link'>Оформить карту по ссылке</a>",
        parse_mode="HTML"
    )

@router.message(F.text == "🏦 Альфа")
async def alfa_info(message: Message):
    await message.answer(
        "🍒 <b>Условия по Альфа-Банку:</b>\n"
        "✅ Бесплатная доставка\n"
        "✅ Кэшбэк до 10%\n\n"
        "👉 <a href='https://example.com/alfa-ref-link'>Оформить карту по ссылке</a>",
        parse_mode="HTML"
    )

@router.message(F.text == "👤 Действующий клиент")
async def existing_client_handler(message: Message):
    await message.answer(
        "🔧 Раздел для действующих клиентов в разработке.\n"
        "🗂️ Скоро здесь появится таблица с продуктами и условиями.",
    )
