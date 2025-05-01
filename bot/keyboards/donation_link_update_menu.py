from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from texts.buttons import GO_BACK_BUTTON


def get_donation_link_update_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=GO_BACK_BUTTON)]
        ],
        resize_keyboard=True
    )
    return keyboard