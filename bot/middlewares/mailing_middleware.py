from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.db import select_all_users
from bot.phrases import admin_id


class MailingMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id == admin_id:  # Admins id
            data['users_ids'] = await select_all_users(data['session_maker'])
            return await handler(event, data)
        else:
            pass
