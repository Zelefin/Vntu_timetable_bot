from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.db.db_functions import check_user
from bot.phrases import reg_mdlwr_phrases
from ScrapItUp import groups_ids


# Это будет inner-мидлварь на сообщения
class RegistrationMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_check = await check_user(data['session_maker'], event.from_user.id)
        if user_check is None:
            return await handler(event, data)
        else:
            await event.answer(reg_mdlwr_phrases["message_ans"].format(g=[key for key, value in groups_ids.items()
                                                                          if value == str(user_check['group'])][0],
                                                                       s=user_check['subgroup']))
