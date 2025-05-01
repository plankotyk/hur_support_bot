from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from texts.buttons import GO_BACK_BUTTON


def get_humanitarian_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=GO_BACK_BUTTON)]
        ],
        resize_keyboard=True
    )
    return keyboard