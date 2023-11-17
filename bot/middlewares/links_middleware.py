from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db.db_functions import check_role
from bot.phrases import links_mdlwr_phrases


class LinksMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject,  Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        check = await check_role(data['session_maker'], event.from_user.id)
        if check:
            data['president_group'] = check
            return await handler(event, data)
        else:
            await event.answer(text=links_mdlwr_phrases['not_president'])
