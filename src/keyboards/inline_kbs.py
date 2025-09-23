from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ease_link_kb():
    inline_kb_list = [
        [
            InlineKeyboardButton(
                text="Генерировать пользователя", callback_data="get_person"
            )
        ],
        [InlineKeyboardButton(text="На главную", callback_data="back_home")],
        [
            InlineKeyboardButton(
                text="Мой хабр", url="https://habr.com/ru/users/yakvenalex/"
            )
        ],
        [
            InlineKeyboardButton(
                text="Веб приложение",
                web_app=WebAppInfo(url="https://airportcards.ru"),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
