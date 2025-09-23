from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.types import CallbackQuery

from src.utils.make_faker import get_random_person
from src.keyboards.all_kb import main_kb, create_space_kb, create_rat
from src.keyboards.inline_kbs import ease_link_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    command_arg: str = command.args  # https://t.me/your_bot?start=hi -> args="hi"
    if command_arg:
        await message.answer(
            f"Запуск сообщения по команде /start with command_arg: {command_arg}",
            reply_markup=main_kb(message.from_user.id),
        )
    else:
        await message.answer(
            "Запуск сообщения по команде /start without command_arg",
            reply_markup=main_kb(message.from_user.id),
        )


@router.message(Command("next"))
async def cmd_start_1(message: Message):
    await message.answer(
        "Запуск сообщения по команде /next", reply_markup=create_space_kb()
    )


@router.message(F.text == "/help")
async def cmd_start_2(message: Message):
    await message.answer("Запуск сообщения по команде /help", reply_markup=create_rat())


@router.message(F.text == "Давай инлайн!")
async def get_inline_btn_link(message: Message):
    await message.answer(
        "Вот тебе инлайн клавиатура со ссылками!", reply_markup=ease_link_kb()
    )


@router.callback_query(F.data == "get_person")
async def send_random_person(call: CallbackQuery):
    # call.answer для возврата ответа, чтобы не мигала кнопка вызова callback
    await call.answer("Генерирую случайного пользователя", show_alert=False)
    user = get_random_person()
    formatted_message = (
        f"👤 <b>Имя:</b> {user['name']}\n"
        f"🏠 <b>Адрес:</b> {user['address']}\n"
        f"📧 <b>Email:</b> {user['email']}\n"
        f"📞 <b>Телефон:</b> {user['phone_number']}\n"
        f"🎂 <b>Дата рождения:</b> {user['birth_date']}\n"
        f"🏢 <b>Компания:</b> {user['company']}\n"
        f"💼 <b>Должность:</b> {user['job']}\n"
    )
    await call.message.answer(formatted_message)


@router.callback_query(F.data == "back_home")
async def back_to_home(callback: CallbackQuery):
    # Удаляем предыдущее сообщение с инлайн клавиатурой
    await callback.message.delete()

    # Отправляем главное меню
    await callback.message.answer(
        "Добро пожаловать на главную страницу!",
        reply_markup=main_kb(callback.from_user.id),
    )

    # Подтверждаем обработку callback
    await callback.answer()
