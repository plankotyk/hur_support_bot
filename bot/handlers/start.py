import logging
from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states.support_form import SupportForm
from bot.keyboards.start_menu import get_start_menu
from texts.texts import WELCOME_TEXT, EXCEPTION_TEXT, UNEXPECTED_EXCEPTION_TEXT

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    try:
        await message.answer(WELCOME_TEXT, reply_markup=get_start_menu(message.from_user.id))
        await state.set_state(SupportForm.waiting_for_initial_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in start_command: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in start_command: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)