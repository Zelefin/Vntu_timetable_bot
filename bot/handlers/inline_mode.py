from aiogram import Router, Bot, F
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from bot.keyboards.user import share_button
from infrastructure.vntu_timetable_api import VntuTimetableApi

inline_mode_router = Router()


@inline_mode_router.inline_query(F.query.regexp(r"^\d+\_\d+$"))
async def handle_inline_query(
    inline_query: InlineQuery, bot: Bot, api: VntuTimetableApi
):
    faculty_id, group_id = [int(value) for value in inline_query.query.split("_")]
    bot_info = await bot.get_me()
    response, faculties = await api.get_faculties()
    if response != 200:
        return

    group_name = None
    for faculty in faculties["data"]:
        if faculty["id"] == faculty_id:
            for group in faculty["groups"]:
                if group["id"] == group_id:
                    group_name = group["name"]
                    break
    if group_name:
        answer = [
            InlineQueryResultArticle(
                id="share_article",
                title="Натисніть тут щоб поділитися!",
                description=f"Поділіться зручним web app для перегляду розкладу групи {group_name}",
                input_message_content=InputTextMessageContent(
                    message_text=f"<b>Розклад для групи "
                    f"<a href='https://t.me/{bot_info.username}/timetable?startapp={faculty_id}_{group_id}'>"
                    f"{group_name}</a></b>"
                ),
                reply_markup=share_button(faculty_id=faculty_id, group_id=group_id),
                thumbnail_url="https://vntu.edu.ua/projects/brandbook/logo11.png",
            )
        ]
    else:
        answer = []

    return inline_query.answer(answer, cache_time=1)
