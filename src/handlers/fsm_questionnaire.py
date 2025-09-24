import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.core.config import bot
from src.keyboards.all_kb import gender_kb
from src.keyboards.inline_kbs import get_login_tg, check_data
from src.utils.utils import extract_number

router = Router()


class Form(StatesGroup):
    gender = State()
    age = State()
    full_name = State()
    user_login = State()
    photo = State()
    about = State()
    check_state = State()


@router.message(Command("start_questionnaire"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(
            "Привет. Для начала выбери свой пол: ", reply_markup=gender_kb()
        )
    await state.set_state(Form.gender)


@router.message(
    (F.text.lower().contains("мужчина")) | (F.text.lower().contains("женщина")),
    Form.gender,
)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(gender=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(
            "Супер! А теперь напиши сколько тебе полных лет: ",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.set_state(Form.age)


@router.message(F.text, Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(
            "Пожалуйста, выбери вариант из тех что в клавиатуре: ",
            reply_markup=gender_kb(),
        )
    await state.set_state(Form.gender)


@router.message(F.text, Form.age)
async def start_questionnaire_process(message: Message, state: FSMContext):
    check_age = extract_number(message.text)

    if not check_age or not (1 <= int(message.text) <= 100):
        await message.reply(
            "Пожалуйста, введите корректный возраст (число от 1 до 100)."
        )
        return

    await state.update_data(age=check_age)
    await message.answer("Теперь укажите свое полное имя:")
    await state.set_state(Form.full_name)


@router.message(F.text, Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    text = "Теперь укажите ваш логин, который будет использоваться в боте"

    if message.from_user.username:
        text += " или нажмите на кнопку ниже и в этом случае вашим логином будет логин из вашего телеграмм: "
        await message.answer(text, reply_markup=get_login_tg())
    else:
        text += " : "
        await message.answer(text)

    await state.set_state(Form.user_login)


# вариант когда мы берем логин из профиля телеграмм
@router.callback_query(F.data, Form.user_login)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer("Беру логин с телеграмм профиля")
    await call.message.edit_reply_markup(
        reply_markup=None
    )  # убираем кнопку после нажатия
    await state.update_data(user_login=call.from_user.username)
    await call.message.answer(
        "А теперь отправьте фото, которое будет использоваться в вашем профиле: "
    )
    await state.set_state(Form.photo)


# вариант когда мы берем логин из введенного пользователем
@router.message(F.text, Form.user_login)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)
    await message.answer(
        "А теперь отправьте фото, которое будет использоваться в вашем профиле: "
    )
    await state.set_state(Form.photo)


@router.message(F.photo, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("А теперь расскажите пару слов о себе: ")
    await state.set_state(Form.about)


@router.message(F.document.mime_type.startswith("image/"), Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.document.file_id
    await state.update_data(photo=photo_id)
    await message.answer("А теперь расскажите пару слов о себе: ")
    await state.set_state(Form.about)


@router.message(F.document, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, отправьте фото!")
    await state.set_state(Form.photo)


@router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    data = await state.get_data()

    caption = (
        f"Пожалуйста, проверьте все ли верно: \n\n"
        f'<b>Полное имя</b>: {data.get("full_name")}\n'
        f'<b>Пол</b>: {data.get("gender")}\n'
        f'<b>Возраст</b>: {data.get("age")} лет\n'
        f'<b>Логин в боте</b>: {data.get("user_login")}\n'
        f'<b>О себе</b>: {data.get("about")}'
    )

    await message.answer_photo(
        photo=data.get("photo"), caption=caption, reply_markup=check_data()
    )
    await state.set_state(Form.check_state)


# сохраняем данные
@router.callback_query(F.data == "correct", Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer("Данные сохранены")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Благодарю за регистрацию. Ваши данные успешно сохранены!"
    )
    await state.clear()


# запускаем анкету сначала
@router.callback_query(F.data == "incorrect", Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer("Запускаем сценарий с начала")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Привет. Для начала выбери свой пол: ", reply_markup=gender_kb()
    )
    await state.set_state(Form.gender)
