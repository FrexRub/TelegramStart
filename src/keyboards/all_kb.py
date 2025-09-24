from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.core.config import setting


def main_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [
            KeyboardButton(text="Давай инлайн!"),
            KeyboardButton(text="Профиль"),
        ],  # строка 1
        [
            KeyboardButton(text="Заполнить анкету"),
            KeyboardButton(text="Каталог"),
        ],  # строка 2
    ]
    if user_telegram_id == setting.bot.admin_id:
        kb_list.append([KeyboardButton(text="Админ панель")])

    # создание клавиатуры из списка объектов KeyboardButton
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard


def create_space_kb():
    kb_list = [
        [KeyboardButton(text="Отправить гео", request_location=True)],
        [KeyboardButton(text="Поделиться номером", request_contact=True)],
        [
            KeyboardButton(
                text="Отправить викторину/опрос", request_poll=KeyboardButtonPollType()
            )
        ],
    ]
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь специальной клавиатурой",
    )
    return keyboard


def create_rat():
    builder = ReplyKeyboardBuilder()
    for item in [str(i) for i in range(1, 11)]:
        builder.button(text=item)
    builder.button(text="Назад")
    builder.adjust(4, 4, 2, 1)  # кол-во кнопок по строкам
    return builder.as_markup(resize_keyboard=True)


def gender_kb():
    kb_list = [
        [KeyboardButton(text="👨‍🦱Мужчина")],
        [KeyboardButton(text="👩‍🦱Женщина")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери пол:",
    )
    return keyboard
