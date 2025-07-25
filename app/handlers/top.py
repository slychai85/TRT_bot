from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text == "🏆 Топ лучших")
async def top_handler(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏆 Перейти в чат", url="https://t.me/+Q44BSTscN7kxNTFi")]
        ]
    )
    await message.answer("🏆 Перейди в чат и выбери интересующий топик:", reply_markup=kb)
