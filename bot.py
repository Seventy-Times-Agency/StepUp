import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database.db import init_db
from handlers import start, courses, learning


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # learning должен быть первым — он перехватывает сообщения во время урока
    dp.include_router(learning.router)
    dp.include_router(start.router)
    dp.include_router(courses.router)

    await init_db()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
