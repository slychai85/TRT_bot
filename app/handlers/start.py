from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.methods import GetChatMember
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from random import randint
from app.keyboards.reply import main_menu
from app.database.models import User
from app.database.session import async_session
from sqlalchemy import select, update
from datetime import datetime

router = Router()
MAIN_CHANNEL = "@TRT_support_bot"


class StartState(StatesGroup):
    awaiting_captcha = State()


# /start — обработка входа
@router.message(F.text.startswith("/start"))
async def start_handler(message: Message, state: FSMContext):
    referral_id = None
    parts = message.text.split()
    if len(parts) == 2 and parts[1].isdigit():
        referral_id = int(parts[1])

    # Проверка подписки
    chat_member = await message.bot(GetChatMember(chat_id=MAIN_CHANNEL, user_id=message.from_user.id))
    if chat_member.status not in ("member", "administrator", "creator"):
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔄 Проверить подписку")]],
            resize_keyboard=True
        )
        await message.answer(
            "⚠️ Подключись к главному каналу: @TRT_support_bot\n\n"
            "Только так ты будешь в курсе планов и развития. Без этой связи ты — просто турист.",
            reply_markup=kb
        )
        return

    # Капча
    a, b = randint(1, 9), randint(1, 9)
    await state.update_data(captcha=a + b, referral_id=referral_id)
    await state.set_state(StartState.awaiting_captcha)
    await message.answer(f"🧠 Для подтверждения, что ты не бот, реши пример:\n\n<b>{a} + {b}</b> = ?")


# Ответ на капчу
@router.message(StartState.awaiting_captcha, F.text.regexp(r"^\d+$"))
async def check_captcha(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data.get("captcha")
    referral_id = data.get("referral_id")

    if int(message.text) != correct_answer:
        await message.answer("❌ Неверно. Попробуй ещё раз.")
        return

    # Проверяем наличие пользователя в базе
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name,
                created_at=datetime.utcnow(),
                joined_at=datetime.utcnow()
            )
            session.add(new_user)
            await session.flush()

            # Если есть реферальный ID — обновим пригласившего
            if referral_id and referral_id != message.from_user.id:
                ref_stmt = select(User).where(User.telegram_id == referral_id)
                ref_result = await session.execute(ref_stmt)
                ref_user = ref_result.scalar_one_or_none()

                if ref_user:
                    ref_user.referrals_count += 1
                    ref_user.referrals_week += 1

        await session.commit()

    await state.clear()
    await message.answer("✅ Подтверждение пройдено. Добро пожаловать в меню!", reply_markup=main_menu)


# Проверка после нажатия "Проверить подписку"
@router.message(F.text == "🔄 Проверить подписку")
async def check_subscription_again(message: Message):
    chat_member = await message.bot(GetChatMember(chat_id=MAIN_CHANNEL, user_id=message.from_user.id))
    if chat_member.status in ("member", "administrator", "creator"):
        await message.answer("✅ Отлично! Теперь снова введи /start для запуска.")
    else:
        await message.answer("❗ Ты всё ещё не подписан. Подключись: @TRT_support_bot")
