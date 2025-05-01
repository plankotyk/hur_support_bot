# welcome
from bot.dtos.appeal_dto import AppealDTO

WELCOME_TEXT = (
    "Привіт, це бот команди ГУР МО А-0458 Support Group.\n\n"
    "Якщо ви бажаєте допомогти військовим або цивільним, створіть звернення.\n\n"
    "Ми обробимо ваше звернення та зв'яжемось з вами."
)
WELCOME_ADMIN_TEXT = "Оберіть команду."

# admin
NO_APPEALS_TEXT = "Звернень поки немає."
ALL_APPEALS_TEXT = "Всі звернення:\n\n"
LAST_10_APPEALS_TEXT = "Останні 10 звернень:\n\n"

def APPEAL_DISPLAY_TEXT(appeal: AppealDTO) -> str:
    return (
        f"ID: {appeal.id[:8]}\n"
        f"Користувач: {appeal.profile_link}\n"
        f"Напрямок: {appeal.direction}\n"
        f"Повідомлення: {appeal.message}\n"
        f"Дата: {appeal.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )

SEND_NEW_DONATE_DESCRIPTION_TEXT = "Надішліть новий опис для донату."
SEND_NEW_DONATE_LINK_TEXT = "Надішліть нове посилання для донату."

def KEY_VALUE_UPDATED_TEXT(key: str) -> str:
    return f"Значення '{key}' оновлено."

# humanitarian
HUMANITARIAN_DIRECTION_DESCRIPTION_TEXT = (
    "Наша команда займається такими цивільними структурами: дитячі садочки, "
    "інтернати для дітей з обмеженими можливостями та медичні заклади.\n\n"
    "Будь ласка, опишіть, чим ви бажаєте допомогти."
)

# military
MILITARY_DIRECTION_DESCRIPTION_TEXT = "Ви хочете долучитися до збору коштів чи допомогти напряму?"
MILITARY_DIRECTION_HELP_DESCRIPTION_TEXT = "Будь ласка, опишіть, чим саме ви бажаєте допомогти."

# other
OTHER_DIRECTION_DESCRIPTION_TEXT = "Будь ласка, опишіть, чим саме ви бажаєте нам допомогти."

# choose
CHOOSE_DIRECTION_TEXT = "Будь ласка, оберіть напрямок."
CHOOSE_OPTION_FROM_MENU_TEXT = "Будь ласка, оберіть опцію з меню."

# permissions
NO_PERMISSION_TEXT = "У вас немає прав для використання цієї команди."

# thank you
THANK_YOU_TEXT = "Дякуємо за підтримку України!"

def THANK_YOU_POST_APPEAL_TEXT(appeal_id: str) -> str:
    return (
        f"Дякуємо за підтримку України!\n"
        f"Ми зв'яжемось з вами.\n"
        f"Номер вашого звернення: #{appeal_id}"
    )

# exceptions
EXCEPTION_TEXT = "Вибачте, сталася помилка. Спробуйте пізніше."
UNEXPECTED_EXCEPTION_TEXT = "Вибачте, сталася неочікувана помилка. Спробуйте ще раз."