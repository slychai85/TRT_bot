from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, desc, func, and_
from app.database.models import User
from app.database.session import async_session
from datetime import datetime, timedelta

router = Router()

TOP_LIMIT = 30  # можно менять при необходимости

# --- Кнопки ---
def get_top_keyboard(current_view: str):
    builder = InlineKeyboardBuilder()
    if current_view == "all":
        builder.button(text="Лучшие за неделю", callback_data="top_week")
    else:
        builder.button(text="Общий ТОП", callback_data="top_all")
    return builder.as_markup()


# --- Команда ТОП ---
@router.message(F.text == "🏆 Топ лучших")
async def show_top(message: Message):
    await send_top(message, view="all")

# --- Обработчики кнопок ---
@router.callback_query(F.data == "top_week")
async def top_week_callback(call: CallbackQuery):
    await call.answer()
    await send_top(call.message, view="week", user_id=call.from_user.id)

@router.callback_query(F.data == "top_all")
async def top_all_callback(call: CallbackQuery):
    await call.answer()
    await send_top(call.message, view="all", user_id=call.from_user.id)

# --- Генерация списка ТОПа ---
async def send_top(message: Message, view: str = "all", user_id: int = None):
    async with async_session() as session:
        stmt = select(User)

        if view == "week":
            one_week_ago = datetime.utcnow() - timedelta(days=7)
            stmt = stmt.where(User.joined_at >= one_week_ago)  # Предполагается, что есть поле joined_at

        stmt = stmt.order_by(desc(User.referrals_count))
        result = await session.execute(stmt)
        users = result.scalars().all()

        top_users = users[:TOP_LIMIT]
        user_map = {user.telegram_id: user for user in users}

        lines = ["<b>🏆 Топ по рефералам:</b>\n"]

        current_user = user_map.get(user_id or message.from_user.id)
        current_in_top = False

        for i, user in enumerate(top_users, 1):
            name = user.full_name or user.username or "Без имени"
            line = f"{i}. {name} — {user.referrals_count}"

            if user.telegram_id == (user_id or message.from_user.id):
                line += " ✅"  # галочка
                current_in_top = True
            lines.append(line)

        if not current_in_top and current_user:
            # Найдём позицию текущего пользователя
            for index, user in enumerate(users, 1):
                if user.telegram_id == current_user.telegram_id:
                    lines.append("...\n<b>Ваша позиция:</b>")
                    name = current_user.full_name or current_user.username or "Вы"
                    lines.append(f"{index}. {name} — {current_user.referrals_count} ✅")
                    break

        await message.answer("\n".join(lines), reply_markup=get_top_keyboard(view))
