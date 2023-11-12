from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.db.db_functions import check_role


class LinksMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        check = await check_role(data['session_maker'], event.from_user.id)
        if check:
            data['president_group'] = check
            return await handler(event, data)
        else:
            pass
