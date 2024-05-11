from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from redis.asyncio import Redis

from bot.handlers.common.faculties_groups import get_faculties, find_group
from bot.keyboards.user import share_button
from infrastructure.vntu_timetable_api import VntuTimetableApi

inline_mode_router = Router()


@inline_mode_router.inline_query()
async def handle_inline_query(
    inline_query: InlineQuery, api: VntuTimetableApi, redis: Redis, bot_username: str
):
    faculties = await get_faculties(redis=redis, api=api)
    faculty_id, group_id, group_name = find_group(
        faculties=faculties, group_name=inline_query.query
    )

    answer = (
        [
            InlineQueryResultArticle(
                id="share_article",
                title="Натисніть тут щоб поділитися!",
                description="Поділіться Web App для перегляду"
                f" розкладу групи {group_name}",
                input_message_content=InputTextMessageContent(
                    message_text=f"<b>Розклад для групи "
                    f"<a href='https://t.me/{bot_username}/timetable"
                    f"?startapp={faculty_id}_{group_id}'>"
                    f"{group_name}</a></b>"
                ),
                reply_markup=share_button(group_name=group_name),
                thumbnail_url="https://i.ibb.co/dDrW9P0/logo10-1.jpg",
            )
        ]
        if faculty_id
        else []
    )

    return inline_query.answer(answer, cache_time=86400)
