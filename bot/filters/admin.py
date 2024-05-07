from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):
    """Filter for admin commands."""

    async def __call__(self, obj: Message, admin_id: int) -> bool:
        return obj.from_user.id == admin_id
