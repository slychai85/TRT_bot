from aiogram import Router, F
from aiogram.types import Message
from app.keyboards.reply import main_menu

router = Router()

@router.message(F.text == "/menu")
async def menu_handler(message: Message):
    await message.answer("📋 Главное меню:", reply_markup=main_menu)
