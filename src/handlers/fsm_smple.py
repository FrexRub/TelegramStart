import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.core.config import bot
from src.utils.utils import extract_number

router = Router()


class Form(StatesGroup):
    name = State()
    age = State()


@router.message(Command("start_quest"))
async def start_quest_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer("Привет. Напиши как тебя зовут: ")
    await state.set_state(Form.name)


@router.message(F.text, Form.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer("Супер! А теперь напиши сколько тебе полных лет: ")
    await state.set_state(Form.age)


@router.message(F.text, Form.age)
async def capture_age(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= check_age <= 100):
        await message.reply(
            "Пожалуйста, введите корректный возраст (число от 1 до 100)."
        )
        return
    await state.update_data(age=check_age)

    data = await state.get_data()
    msg_text = (
        f'Вас зовут <b>{data.get("name")}</b> и вам <b>{data.get("age")}</b> лет. '
        f"Спасибо за то что ответили на мои вопросы."
    )
    await message.answer(msg_text)
    await state.clear()
