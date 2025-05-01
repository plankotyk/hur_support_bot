from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from texts.buttons import GO_BACK_BUTTON, ALL_APPEALS_BUTTON, LAST_10_APPEALS_BUTTON, CHANGE_DONATE_DESCRIPTION_BUTTON, \
    CHANGE_DONATE_LINK_BUTTON


def get_admin_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ALL_APPEALS_BUTTON)],
            [KeyboardButton(text=LAST_10_APPEALS_BUTTON)],
            [KeyboardButton(text=CHANGE_DONATE_DESCRIPTION_BUTTON)],
            [KeyboardButton(text=CHANGE_DONATE_LINK_BUTTON)],
            [KeyboardButton(text=GO_BACK_BUTTON)],
        ],
        resize_keyboard=True
    )
    return keyboard