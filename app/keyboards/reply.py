from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Реф. программа"), KeyboardButton(text="📞 Поддержка")],
        [KeyboardButton(text="💬 Отзывы"), KeyboardButton(text="🏆 Топ лучших")],
        [KeyboardButton(text="👤 Мой профиль"), KeyboardButton(text="🚀 Как начать")]
    ],
    resize_keyboard=True
)
