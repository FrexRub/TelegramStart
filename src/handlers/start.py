from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup

from src.keyboards.all_kb import main_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Запуск сообщения по команде /start", reply_markup=main_kb(message.from_user.id)
    )


@router.message(Command("next"))
async def cmd_start_2(message: Message):
    await message.answer("Запуск сообщения по команде /next")


@router.message(F.text == "/help")
async def cmd_start_2(message: Message):
    await message.answer("Запуск сообщения по команде /help")
