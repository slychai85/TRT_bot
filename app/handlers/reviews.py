from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text == "💬 Отзывы")
async def reviews_handler(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Перейти", url="https://t.me/c/2891941417/3")]
        ]
    )
    await message.answer("📢 Чат с отзывами:", reply_markup=kb)
