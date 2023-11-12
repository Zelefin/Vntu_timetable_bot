from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.db.db_functions import check_user, check_user_vis, add_user_vis
from bot.phrases import start_midlwr_phrases


# Это будет inner-мидлварь на сообщения
class StartMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if await check_user_vis(data['session_maker'], event.from_user.id):
            user_check = await check_user(data['session_maker'], event.from_user.id)
            if user_check is not None:
                data['user_info'] = user_check
                return await handler(event, data)
            else:
                data['user_info'] = False
                return await handler(event, data)
        else:
            await add_user_vis(data['session_maker'], event.from_user.id)
            await event.answer(start_midlwr_phrases["first_visit"].format(n=event.from_user.first_name))
