import asyncio
import logging

from src.core.config import configure_logging, bot, dp
from src.handlers.start import router as start_router
from src.core.commands import set_commands

configure_logging(logging.INFO)
logger = logging.getLogger(__name__)

dp.include_router(start_router)


async def on_startup():
    await set_commands()


async def main():
    logger.info("Start Bot")
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
