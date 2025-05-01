import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher
from bot.handlers import start, direction
from bot.database.db import init_db, close_pool
from config.config import BOT_TOKEN

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

log_handler = TimedRotatingFileHandler(
    "bot.log", when="D", interval=3, backupCount=3
)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()  # root logger
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(start.router, direction.router)

    await init_db()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        try:
            await close_pool()
        except Exception as e:
            logger.error(f"Error closing database pool: {e}")

if __name__ == "__main__":
    asyncio.run(main())