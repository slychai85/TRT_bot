import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
import os
from app.handlers import menu, referral, support, start, reviews, top


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(referral.router)
    dp.include_router(support.router)
    dp.include_router(reviews.router)
    dp.include_router(top.router)

    # Регистрируем хендлеры (позже)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
