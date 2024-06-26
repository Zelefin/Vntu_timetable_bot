import asyncio
import logging

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup

from infrastructure.database.repo.requests import RequestsRepo


async def send_message(
    bot: Bot,
    user_id: int | str,
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    """
    Safe messages sender

    :param bot: Bot instance.
    :param user_id: user id. If str - must contain only digits.
    :param text: text of the message.
    :param reply_markup: reply markup.
    :return: success.
    """
    try:
        await bot.send_message(
            user_id,
            text,
            reply_markup=reply_markup,
        )
    except exceptions.TelegramBadRequest:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error("Target [ID:%i]: got TelegramForbiddenError", user_id)
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            "Target [ID:%i]: Flood limit is exceeded. Sleep %i seconds.",
            user_id,
            e.retry_after,
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(bot, user_id, text, reply_markup)  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception("Target [ID:%i]: failed", user_id)
    else:
        logging.info("Target [ID:%i]: success", user_id)
        return True
    return False


async def broadcast(
    bot: Bot,
    users: list[str | int],
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
    repo: RequestsRepo | None = None,
) -> int:
    """
    Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param text: Text of the message.
    :param reply_markup: Reply markup.
    :param repo: Database repository.
    :return: Count of messages.
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(bot, user_id, text, reply_markup):
                count += 1
            else:
                if repo:
                    await repo.users.inactive_user(user_id=user_id)
            await asyncio.sleep(
                0.05
            )  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info("%i messages successful sent.", count)

    return count
