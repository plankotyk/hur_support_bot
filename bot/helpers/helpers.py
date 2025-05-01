import logging

from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramAPIError

from bot.dtos.appeal_dto import AppealDTO
from config.config import ADMIN_CHANNEL_ID


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
        logger.info(f"Successfully notified channel about appeal {appeal.id}")
    except TelegramForbiddenError as e:
        logger.error(f"Cannot send message to channel {ADMIN_CHANNEL_ID}: Bot is blocked or lacks permission - {e}")
    except TelegramBadRequest as e:
        logger.error(f"Invalid request to channel {ADMIN_CHANNEL_ID} for appeal {appeal.id}: {e}")
    except TelegramAPIError as e:
        logger.error(f"Telegram API error for appeal {appeal.id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error notifying channel about appeal {appeal.id}: {e}")
