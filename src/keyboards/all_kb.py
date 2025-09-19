from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.core.config import setting


def main_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="О нас"), KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Заполнить анкету"), KeyboardButton(text="Каталог")],
    ]
    if user_telegram_id == setting.bot.admin_id:
        kb_list.append([KeyboardButton(text="Админ панель")])

    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard
