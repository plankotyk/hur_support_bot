from aiogram.fsm.state import State, StatesGroup

class SupportForm(StatesGroup):
    waiting_for_initial_choice = State()
    waiting_for_direction = State()
    waiting_for_humanitarian_help = State()
    waiting_for_military_choice = State()
    waiting_for_military_help = State()
    waiting_for_donation_message = State()
    waiting_for_donation_link = State()
    waiting_for_other_help = State()
    waiting_for_admin_choice = State()
    waiting_for_post_added_appeal_choice = State()