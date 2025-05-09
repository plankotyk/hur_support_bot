import logging
import os

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramAPIError

from bot.dtos.appeal_dto import AppealDTO
from config.config import ADMIN_CHANNEL_ID, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

import smtplib
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)


def get_user_link(user):
    if user.username:
        return f"https://t.me/{user.username}"
    else:
        return f"tg://user?id={user.id}"


async def notify_channel_about_appeal(bot, appeal: AppealDTO):
    text = (
        f"<b>Звернення</b> <code>{appeal.id}</code>\n"
        f"<b>Створено:</b> {appeal.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"<b>Користувач:</b> {appeal.profile_link}\n"
        f"<b>Напрямок:</b> {appeal.direction}\n"
        f"<b>Повідомлення:</b>\n{appeal.message}"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHANNEL_ID,
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        logger.info(f"Successfully notified about appeal {appeal.id} via telegram")
    except TelegramForbiddenError as e:
        logger.error(f"Cannot send message to channel {ADMIN_CHANNEL_ID}: Bot is blocked or lacks permission - {e}")
    except TelegramBadRequest as e:
        logger.error(f"Invalid request to channel {ADMIN_CHANNEL_ID} for appeal {appeal.id}: {e}")
    except TelegramAPIError as e:
        logger.error(f"Telegram API error for appeal {appeal.id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error notifying about appeal {appeal.id} via telegram: {e}")


async def notify_email_about_appeal(appeal: AppealDTO):
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD

    text = (
        f"<b>Звернення</b> <code>{appeal.id}</code><br>"
        f"<b>Створено:</b> {appeal.created_at.strftime('%Y-%m-%d %H:%M:%S')}<br>"
        f"<b>Користувач:</b> {appeal.profile_link}<br>"
        f"<b>Напрямок:</b> {appeal.direction}<br>"
        f"<b>Повідомлення:</b>\n{appeal.message}"
    )

    msg = MIMEText(text, 'html')
    msg['Subject'] = appeal.direction
    msg['From'] = sender_email
    receiver_email = RECEIVER_EMAIL
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            logger.info(f"Successfully notified about appeal {appeal.id} via email")
    except smtplib.SMTPAuthenticationError:
        logging.error("Failed to log in to the SMTP server. Check email/password.")
        raise
    except smtplib.SMTPConnectError:
        logging.error("Failed to connect to the SMTP server.")
        raise
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"The recipient {receiver_email} was refused by the server.")
        raise
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error notifying about appeal {appeal.id} via email: {e}")
        raise
