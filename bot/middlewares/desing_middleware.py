from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.db import check_user
from bot.phrases import design_midlwr_phrases


# Это будет inner-мидлварь на сообщения
class DesignMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_check = await check_user(data['session_maker'], event.from_user.id)
        if user_check is not None:
            data['user_info'] = user_check
            return await handler(event, data)
        else:
            await event.answer(design_midlwr_phrases["message_ans"])


class DesignCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_check = await check_user(data['session_maker'], event.from_user.id)
        if user_check is not None:
            data['user_info'] = user_check
            return await handler(event, data)
        else:
            await event.answer(design_midlwr_phrases["callback_ans"])
