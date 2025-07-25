from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "🎁 Реф. программа")
async def referral_handler(message: Message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/TRTsupport_bot?start={user_id}"

    await message.answer(
        f"🎁 Приглашай друзей и получай бонусы!\n\n"
        f"🔗 Твоя реферальная ссылка:\n{ref_link}\n\n"
        f"🎉 Лотерея с призами каждые 2 недели!"
    )
