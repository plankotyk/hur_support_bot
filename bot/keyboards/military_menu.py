from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from texts.buttons import GO_BACK_BUTTON, MILITARY_DIRECTION_DONATE_BUTTON, MILITARY_DIRECTION_DIRECT_HELP_BUTTON


def get_military_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MILITARY_DIRECTION_DONATE_BUTTON)],
            [KeyboardButton(text=MILITARY_DIRECTION_DIRECT_HELP_BUTTON)],
            [KeyboardButton(text=GO_BACK_BUTTON)]
        ],
        resize_keyboard=True
    )
    return keyboard