from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext
from app.states.support import SupportStates

router = Router()
SUPPORT_CHAT_ID = -4837484525  # ID группы поддержки


# Хендлер на кнопку "📞 Поддержка"
@router.message(F.text == "📞 Поддержка")
async def support_handler(message: Message, state: FSMContext):
    await message.answer(
        "✏️ Напишите ваше сообщение и отправьте его.\nОно будет передано в службу поддержки.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SupportStates.waiting_message)


# Получение обращения от пользователя
@router.message(SupportStates.waiting_message)
async def forward_to_support(message: Message, state: FSMContext):
    await state.clear()

    # Инлайн-кнопка "📩 ОТВЕТИТЬ"
    answer_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 ОТВЕТИТЬ", callback_data=f"answer_to_{message.from_user.id}")]
        ]
    )

    # Подтверждение пользователю
    await message.answer(
        "✅ Сообщение отправлено в поддержку. Ожидайте ответа.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📍 Меню", callback_data="back_to_menu")]
            ]
        )
    )

    # Пересылка в чат поддержки
    text = (
        f"📨 Сообщение от <b>@{message.from_user.username or 'без username'}</b>\n"
        f"ID: <code>{message.from_user.id}</code>\n\n"
        f"{message.text}"
    )
    await message.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=text,
        reply_markup=answer_btn,
        parse_mode="HTML"
    )


# Нажатие на кнопку "📩 ОТВЕТИТЬ" в группе
@router.callback_query(F.data.startswith("answer_to_"))
async def handle_reply_button(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[-1])
    await state.set_state(SupportStates.waiting_reply)
    await state.update_data(reply_to=user_id)

    await callback.message.answer(
        f"✍️ Напишите сообщение для пользователя <code>{user_id}</code>",
        parse_mode="HTML"
    )
    await callback.answer()


# Получение ответа от админа → пересылка пользователю
@router.message(SupportStates.waiting_reply)
async def send_reply_to_user(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("reply_to")
    await state.clear()

    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=f"📬 Ответ от поддержки:\n\n{message.text}"
        )
        await message.answer("✅ Ответ отправлен.")
    except Exception:
        await message.answer("❌ Не удалось отправить сообщение. Возможно, пользователь заблокировал бота.")


# Возврат в меню по кнопке
@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    from app.keyboards.reply import main_menu
    await callback.message.answer("📍 Главное меню", reply_markup=main_menu)
    await callback.answer()
