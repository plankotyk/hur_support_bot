import logging
import smtplib
from datetime import datetime

import asyncpg
from aiogram import Router, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.admin_menu import get_admin_menu
from bot.keyboards.donation_link_update_menu import get_donation_link_update_menu
from bot.keyboards.donation_message_update_menu import get_donation_message_update_menu
from bot.keyboards.main_menu import get_main_menu
from bot.keyboards.military_menu import get_military_menu
from bot.keyboards.humanitarian_menu import get_humanitarian_menu
from bot.keyboards.post_added_appeal_menu import get_post_added_appeal_menu
from bot.keyboards.direct_military_menu import get_direct_military_menu
from bot.keyboards.other_menu import get_other_menu
from bot.keyboards.start_menu import get_start_menu
from bot.states.support_form import SupportForm
from bot.database.db import save_appeal, get_all_appeals, get_last_10_appeals, update_value_by_key, get_value_by_key
from bot.helpers.helpers import get_user_link, notify_email_about_appeal
from uuid import uuid4

from config.config import ADMIN_IDS
from texts.buttons import *
from texts.texts import *

router = Router()
logger = logging.getLogger(__name__)


@router.message(SupportForm.waiting_for_initial_choice)
async def process_initial_choice(message: Message, state: FSMContext):
    try:
        if message.text == CREATE_APPEAL_BUTTON:
            await message.answer(CHOOSE_DIRECTION_TEXT, reply_markup=get_main_menu())
            await state.set_state(SupportForm.waiting_for_direction)
        elif message.text == ADMIN_PANEL_BUTTON:
            if message.from_user.id in ADMIN_IDS:
                await message.answer(WELCOME_ADMIN_TEXT, reply_markup=get_admin_menu())
                await state.set_state(SupportForm.waiting_for_admin_choice)
            else:
                await message.answer(NO_PERMISSION_TEXT, reply_markup=get_admin_menu())
                await message.answer(WELCOME_TEXT, reply_markup=get_start_menu(message.from_user.id))
                await state.set_state(SupportForm.waiting_for_initial_choice)
        else:
            await message.answer(CHOOSE_OPTION_FROM_MENU_TEXT, reply_markup=get_start_menu(message.from_user.id))
            await state.set_state(SupportForm.waiting_for_initial_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_initial_choice: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_initial_choice: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_admin_choice)
async def process_admin_choice(message: Message, state: FSMContext):
    try:
        if message.text == ALL_APPEALS_BUTTON:
            appeals = await get_all_appeals()
            response = NO_APPEALS_TEXT
            if appeals:
                response = ALL_APPEALS_TEXT
                for appeal in appeals:
                    response += APPEAL_DISPLAY_TEXT(appeal)
            await message.answer(response, reply_markup=get_admin_menu(),
                                 disable_web_page_preview=True)
            await state.set_state(SupportForm.waiting_for_admin_choice)
        elif message.text == LAST_10_APPEALS_BUTTON:
            appeals = await get_last_10_appeals()
            response = NO_APPEALS_TEXT
            if appeals:
                response = LAST_10_APPEALS_TEXT
                for appeal in appeals:
                    response += APPEAL_DISPLAY_TEXT(appeal)
            await message.answer(response, reply_markup=get_admin_menu(),
                                 disable_web_page_preview=True)
            await state.set_state(SupportForm.waiting_for_admin_choice)
        elif message.text == CHANGE_DONATE_DESCRIPTION_BUTTON:
            await message.answer(SEND_NEW_DONATE_DESCRIPTION_TEXT, reply_markup=get_donation_message_update_menu())
            await state.set_state(SupportForm.waiting_for_donation_message)
        elif message.text == CHANGE_DONATE_LINK_BUTTON:
            await message.answer(SEND_NEW_DONATE_LINK_TEXT, reply_markup=get_donation_link_update_menu())
            await state.set_state(SupportForm.waiting_for_donation_link)
        elif message.text == GO_BACK_BUTTON:
            await message.answer(WELCOME_TEXT, reply_markup=get_start_menu(message.from_user.id))
            await state.set_state(SupportForm.waiting_for_initial_choice)
        else:
            await message.answer(CHOOSE_OPTION_FROM_MENU_TEXT, reply_markup=get_admin_menu())
            await state.set_state(SupportForm.waiting_for_admin_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_admin_choice: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_admin_choice: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_admin_choice: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_donation_message)
async def process_donation_message_update(message: Message, state: FSMContext):
    try:
        if message.text == GO_BACK_BUTTON:
            await message.answer(WELCOME_ADMIN_TEXT, reply_markup=get_admin_menu())
            await state.set_state(SupportForm.waiting_for_admin_choice)
        else:
            await update_value_by_key('donation_message', message.text)
            await message.answer(KEY_VALUE_UPDATED_TEXT('donation_message'),
                                 reply_markup=get_admin_menu())
            await state.set_state(SupportForm.waiting_for_admin_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_donation_message_update: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_donation_message_update: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_donation_message_update: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_donation_link)
async def process_donation_link_update(message: Message, state: FSMContext):
    try:
        if message.text == GO_BACK_BUTTON:
            await message.answer(WELCOME_ADMIN_TEXT, reply_markup=get_admin_menu())
            await state.set_state(SupportForm.waiting_for_admin_choice)
        else:
            await update_value_by_key('donation_link', message.text)
            await message.answer(KEY_VALUE_UPDATED_TEXT('donation_link'),
                                 reply_markup=get_admin_menu())
            await state.set_state(SupportForm.waiting_for_admin_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_donation_link_update: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_donation_link_update: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_donation_link_update: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_direction)
async def process_direction(message: Message, state: FSMContext):
    try:
        if message.text == HUMANITARIAN_DIRECTION_BUTTON:
            await message.answer(HUMANITARIAN_DIRECTION_DESCRIPTION_TEXT, reply_markup=get_humanitarian_menu())
            await state.set_state(SupportForm.waiting_for_humanitarian_help)
            await state.update_data(direction="humanitarian")

        elif message.text == MILITARY_DIRECTION_BUTTON:
            await message.answer(MILITARY_DIRECTION_DESCRIPTION_TEXT, reply_markup=get_military_menu())
            await state.set_state(SupportForm.waiting_for_military_choice)
            await state.update_data(direction="military")

        elif message.text == OTHER_DIRECTION_BUTTON:
            await message.answer(OTHER_DIRECTION_DESCRIPTION_TEXT, reply_markup=get_other_menu())
            await state.set_state(SupportForm.waiting_for_other_help)
            await state.update_data(direction="other")
        elif message.text == GO_BACK_BUTTON:
            await message.answer(WELCOME_TEXT, reply_markup=get_start_menu(message.from_user.id))
            await state.set_state(SupportForm.waiting_for_initial_choice)
        else:
            await message.answer(CHOOSE_OPTION_FROM_MENU_TEXT, reply_markup=get_main_menu())
            await state.set_state(SupportForm.waiting_for_direction)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_direction: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_direction: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_post_added_appeal_choice)
async def process_post_added_appeal_choice(message: Message, state: FSMContext):
    try:
        if message.text == CREATE_ONE_MORE_APPEAL_BUTTON:
            await message.answer(CHOOSE_DIRECTION_TEXT, reply_markup=get_main_menu())
            await state.set_state(SupportForm.waiting_for_direction)
        elif message.text == GO_BACK_BUTTON:
            await message.answer(WELCOME_TEXT, reply_markup=get_start_menu(message.from_user.id))
            await state.set_state(SupportForm.waiting_for_initial_choice)
        else:
            await message.answer(CHOOSE_OPTION_FROM_MENU_TEXT, reply_markup=get_post_added_appeal_menu())
            await state.set_state(SupportForm.waiting_for_post_added_appeal_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_post_added_appeal_choice: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_post_added_appeal_choice: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)

@router.message(SupportForm.waiting_for_humanitarian_help)
async def process_humanitarian_help(message: Message, state: FSMContext):
    try:
        if message.text == GO_BACK_BUTTON:
            await message.answer(CHOOSE_DIRECTION_TEXT, reply_markup=get_main_menu())
            await state.set_state(SupportForm.waiting_for_direction)
        else:
            user_data = await state.get_data()
            appeal = AppealDTO(
                id=str(uuid4()),
                user_id=message.from_user.id,
                profile_link=get_user_link(message.from_user),
                direction=user_data.get("direction"),
                message=message.text,
                username=message.from_user.username,
                created_at=datetime.now()
            )

            await save_appeal(appeal)

            await notify_email_about_appeal(appeal)
            await message.answer(THANK_YOU_POST_APPEAL_TEXT(appeal.id[:8]), reply_markup=get_post_added_appeal_menu())
            await state.set_state(SupportForm.waiting_for_post_added_appeal_choice)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError,
        smtplib.SMTPRecipientsRefused, smtplib.SMTPException) as e:
        logger.error(f"SMTP error: {e}")
        await message.answer(EXCEPTION_TEXT)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_humanitarian_help: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_humanitarian_help: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_humanitarian_help: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_military_choice)
async def process_military_choice(message: Message, state: FSMContext):
    try:
        if message.text == MILITARY_DIRECTION_DONATE_BUTTON:
            donation_message = await get_value_by_key('donation_message')
            donation_link = await get_value_by_key('donation_link')
            await message.answer(donation_message)
            await message.answer(donation_link)
            await message.answer(THANK_YOU_TEXT, reply_markup=get_post_added_appeal_menu())
            await state.set_state(SupportForm.waiting_for_post_added_appeal_choice)

        elif message.text == MILITARY_DIRECTION_DIRECT_HELP_BUTTON:
            await message.answer(MILITARY_DIRECTION_HELP_DESCRIPTION_TEXT,
                                 reply_markup=get_direct_military_menu())
            await state.set_state(SupportForm.waiting_for_military_help)

        elif message.text == GO_BACK_BUTTON:
            await message.answer(CHOOSE_DIRECTION_TEXT, reply_markup=get_main_menu())
            await state.set_state(SupportForm.waiting_for_direction)
        else:
            await message.answer(CHOOSE_OPTION_FROM_MENU_TEXT, reply_markup=get_military_menu())
            await state.set_state(SupportForm.waiting_for_military_choice)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_military_choice: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_military_choice: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_military_choice: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_military_help)
async def process_military_help(message: Message, state: FSMContext):
    try:
        if message.text == GO_BACK_BUTTON:
            await message.answer(MILITARY_DIRECTION_DESCRIPTION_TEXT, reply_markup=get_military_menu())
            await state.set_state(SupportForm.waiting_for_military_choice)
        else:
            user_data = await state.get_data()
            appeal = AppealDTO(
                id=str(uuid4()),
                user_id=message.from_user.id,
                profile_link=get_user_link(message.from_user),
                direction=user_data.get("direction"),
                message=message.text,
                username=message.from_user.username,
                created_at=datetime.now()
            )

            await save_appeal(appeal)

            await notify_email_about_appeal(appeal)
            await message.answer(THANK_YOU_POST_APPEAL_TEXT(appeal.id[:8]),
                                 reply_markup=get_post_added_appeal_menu())
            await state.set_state(SupportForm.waiting_for_post_added_appeal_choice)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError,
        smtplib.SMTPRecipientsRefused, smtplib.SMTPException) as e:
        logger.error(f"SMTP error: {e}")
        await message.answer(EXCEPTION_TEXT)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_military_help: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_military_help: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_military_help: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)


@router.message(SupportForm.waiting_for_other_help)
async def process_other_help(message: Message, state: FSMContext):
    try:
        if message.text == GO_BACK_BUTTON:
            await message.answer(CHOOSE_DIRECTION_TEXT, reply_markup=get_main_menu())
            await state.set_state(SupportForm.waiting_for_direction)
        else:
            user_data = await state.get_data()
            appeal = AppealDTO(
                id=str(uuid4()),
                user_id=message.from_user.id,
                profile_link=get_user_link(message.from_user),
                direction=user_data.get("direction"),
                message=message.text,
                username=message.from_user.username,
                created_at=datetime.now()
            )

            await save_appeal(appeal)

            await notify_email_about_appeal(appeal)
            await message.answer(THANK_YOU_POST_APPEAL_TEXT(appeal.id[:8]), reply_markup=get_post_added_appeal_menu())
            await state.set_state(SupportForm.waiting_for_post_added_appeal_choice)
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError,
        smtplib.SMTPRecipientsRefused, smtplib.SMTPException) as e:
        logger.error(f"SMTP error: {e}")
        await message.answer(EXCEPTION_TEXT)
    except TelegramAPIError as e:
        logger.error(f"Telegram API error in process_other_help: {e}")
        await message.answer(EXCEPTION_TEXT)
    except asyncpg.exceptions.PostgresError as e:
        logger.error(f"Postgres error in process_other_help: {e}")
        await message.answer(EXCEPTION_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in process_other_help: {e}")
        await message.answer(UNEXPECTED_EXCEPTION_TEXT)
