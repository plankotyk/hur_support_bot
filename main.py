import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher
from bot.handlers import start, direction
from bot.database.db import init_db, close_pool
from config.config import BOT_TOKEN

log_handler = TimedRotatingFileHandler("bot.log", when="D", interval=3, backupCount=3)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
console_handler = logging.StreamHandler()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

async def main():
    logger.info("Starting application...")
    logger.info(f"BOT_TOKEN is set: {'True' if BOT_TOKEN else 'False'}")

    try:
        logger.info("Initializing bot...")
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()

        logger.info("Including routers...")
        dp.include_routers(start.router, direction.router)

        logger.info("Initializing database...")
        await init_db()

        logger.info("Starting bot polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Closing bot session and database pool...")
        await bot.session.close()
        try:
            await close_pool()
        except Exception as e:
            logger.error(f"Error closing database pool: {e}")

if __name__ == "__main__":
    logger.info("Entering main script...")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}", exc_info=True)
        exit(1)