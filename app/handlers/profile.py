from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from sqlalchemy import select
from app.database.session import async_session
from app.database.models import User

router = Router()

@router.message(F.text == "👤 Мой профиль")
async def show_profile(message: Message):
    user_id = message.from_user.id

    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()

    if not user:
        await message.answer("❗ Пользователь не найден в базе.")
        return

    text = (
        f"<b>👤 Профиль:</b>\n"
        f"🆔 <b>ID:</b> <code>{user.telegram_id}</code>\n"
        f"👥 <b>Приглашённых:</b> {user.referrals_count}\n"
        f"💸 <b>Заработано:</b> 0 SOL\n"
        f"🔗 Реф.ссылка:\n https://t.me/TRT_support_bot?start={user.telegram_id}"
    )

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Вывести на Sol", callback_data="withdraw_disabled")]
    ])

    await message.answer(text, reply_markup=buttons)

@router.callback_query(F.data == "withdraw_disabled")
async def handle_withdraw(callback: CallbackQuery):
    await callback.answer("🚧 Вывод скоро будет доступен", show_alert=True)