from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.config_reader import Config


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.from_user.id == config.admin) == self.is_admin
