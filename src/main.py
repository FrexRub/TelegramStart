import asyncio
import logging

from src.core.config import configure_logging, bot, dp
from src.handlers.start import router as start_router
from src.core.commands import set_commands

configure_logging(logging.INFO)
logger = logging.getLogger(__name__)

dp.include_router(start_router)


async def main():
    logger.info("Start Bot")
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    asyncio.run(main())
