from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Запуск сообщения по команде /start")


@router.message(Command("next"))
async def cmd_start_2(message: Message):
    await message.answer("Запуск сообщения по команде /next")
