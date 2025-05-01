from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.config import ADMIN_IDS
from texts.buttons import CREATE_APPEAL_BUTTON, ADMIN_PANEL_BUTTON


def get_start_menu(user_id: int):
    keyboard_buttons = [
        [KeyboardButton(text=CREATE_APPEAL_BUTTON)]
    ]
    if user_id in ADMIN_IDS:
        keyboard_buttons.append([KeyboardButton(text=ADMIN_PANEL_BUTTON)])

    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_buttons,
        resize_keyboard=True
    )
    return keyboard