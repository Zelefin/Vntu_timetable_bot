import json

from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from redis.asyncio import Redis

from bot.keyboards.user import share_button
from infrastructure.vntu_timetable_api import VntuTimetableApi

inline_mode_router = Router()


@inline_mode_router.inline_query()
async def handle_inline_query(
    inline_query: InlineQuery, api: VntuTimetableApi, redis: Redis, bot_username: str
):
    group_name = inline_query.query
    if faculties_redis := await redis.get("faculties"):
        faculties = json.loads(faculties_redis)
    else:
        response, faculties = await api.get_faculties()
        if response != 200 or not faculties:
            return
        await redis.set("faculties", json.dumps(faculties), ex=1800)

    faculty_id: str | None = None
    group_id: str | None = None
    group_name_normalized: str | None = None
    for faculty in faculties.get("data"):
        for group in faculty["groups"]:
            if group["name"].upper() == group_name.upper():
                faculty_id = faculty["id"]
                group_id = group["id"]
                group_name_normalized = group["name"]
                break
            if faculty_id:
                break

    answer = (
        [
            InlineQueryResultArticle(
                id="share_article",
                title="Натисніть тут щоб поділитися!",
                description="Поділіться Web App для перегляду"
                f" розкладу групи {group_name_normalized}",
                input_message_content=InputTextMessageContent(
                    message_text=f"<b>Розклад для групи "
                    f"<a href='https://t.me/{bot_username}/timetable"
                    f"?startapp={faculty_id}_{group_id}'>"
                    f"{group_name_normalized}</a></b>"
                ),
                reply_markup=share_button(group_name=group_name_normalized),
                thumbnail_url="https://i.ibb.co/dDrW9P0/logo10-1.jpg",
            )
        ]
        if faculty_id
        else []
    )

    return inline_query.answer(answer, cache_time=86400)
