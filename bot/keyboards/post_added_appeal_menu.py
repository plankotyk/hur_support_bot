from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from texts.buttons import GO_BACK_BUTTON, CREATE_ONE_MORE_APPEAL_BUTTON


def get_post_added_appeal_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CREATE_ONE_MORE_APPEAL_BUTTON)],
            [KeyboardButton(text=GO_BACK_BUTTON)],
        ],
        resize_keyboard=True
    )
    return keyboard