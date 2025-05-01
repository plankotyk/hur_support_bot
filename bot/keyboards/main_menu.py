from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from texts.buttons import GO_BACK_BUTTON, HUMANITARIAN_DIRECTION_BUTTON, MILITARY_DIRECTION_BUTTON, \
    OTHER_DIRECTION_BUTTON


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=HUMANITARIAN_DIRECTION_BUTTON)],
            [KeyboardButton(text=MILITARY_DIRECTION_BUTTON)],
            [KeyboardButton(text=OTHER_DIRECTION_BUTTON)],
            [KeyboardButton(text=GO_BACK_BUTTON)]
        ],
        resize_keyboard=True
    )
    return keyboard