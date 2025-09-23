from aiogram.types import BotCommand, BotCommandScopeDefault

from src.core.config import bot


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
        BotCommand(command="next", description="Спец. клавиатура"),
        BotCommand(command="help", description="Опрос"),
        BotCommand(command="faq", description="Частые вопросы"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
