import asyncio
from aiogram import Bot, Dispatcher, F

from bot_route import route
from config import telegram_config
from database import create_table
from database_utils import init_role_passwords
from logger import logger_config

bot = Bot(token=telegram_config['telegram_token_api'])
dp = Dispatcher()
dp.include_router(route)


# Launching a telegram bot and other functions
async def main():
    logger = await logger_config(name="main", log_file="bot_core.log")
    try:
        await create_table()
        await init_role_passwords()
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(ex)


if __name__ == '__main__':
    asyncio.run(main())
