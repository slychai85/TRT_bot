from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.methods import GetChatMember
from aiogram.fsm.context import FSMContext
from random import randint
from app.keyboards.reply import main_menu

router = Router()
MAIN_CHANNEL = "@TRT_support_bot"  # основной канал


# /start — проверка подписки и логика входа
@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    # Проверка подписки
    chat_member = await message.bot(GetChatMember(chat_id=MAIN_CHANNEL, user_id=message.from_user.id))
    if chat_member.status not in ("member", "administrator", "creator"):
        # Не подписан — просим подписаться
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

    # Если подписан и уже верифицирован — сразу меню
    data = await state.get_data()
    if data.get("verified"):
        await message.answer("📋 Главное меню:", reply_markup=main_menu)
        return

    # Иначе — капча
    a, b = randint(1, 9), randint(1, 9)
    await state.update_data(captcha=a + b)
    await message.answer(f"🧠 Для подтверждения, что ты не бот, реши пример:\n\n<b>{a} + {b}</b> = ?")


# Ответ на капчу
@router.message(F.text.regexp(r"^\d+$"))
async def check_captcha(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data.get("captcha")

    if correct_answer is None:
        return  # капча не запрошена

    if int(message.text) == correct_answer:
        # Верно — сохраняем флаг, удаляем капчу и показываем меню
        await state.update_data(verified=True, captcha=None)
        await message.answer("✅ Подтверждение пройдено. Добро пожаловать в меню!", reply_markup=main_menu)
    else:
        await message.answer("❌ Неверно. Попробуй ещё раз.")


# Проверить подписку после кнопки
@router.message(F.text == "🔄 Проверить подписку")
async def check_again(message: Message):
    chat_member = await message.bot(GetChatMember(chat_id=MAIN_CHANNEL, user_id=message.from_user.id))
    if chat_member.status in ("member", "administrator", "creator"):
        await message.answer("✅ Отлично! Теперь снова введи /start для запуска.")
    else:
        await message.answer("❗ Ты всё ещё не подписан. Подключись: @TRT_support_bot")
