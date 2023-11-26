from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from bot.Groups_func import send_lessons
from ScrapItUp.ids_dict import groups_ids
from bot.days_weeks_stuff import cur_day, cur_week

inline_router = Router(name='inline')

chikiponponi = [
    "1ПІ-23б",
    "2ПІ-23б",
    "3ПІ-23б",
    "4ПІ-23б",
    "5ПІ-23б",
    "6ПІ-23б"
]


async def search_group(prefix: str, groups: list[str]) -> list[str]:
    result = [group for group in groups if prefix in group]
    return result


@inline_router.inline_query()
async def show_user_links(inline_query: InlineQuery):
    text = inline_query.query.upper() if len(inline_query.query) > 1 else ""
    matching_groups: list[str] = await search_group(text, chikiponponi)

    if matching_groups and len(matching_groups) < 2:
        answer = [
            InlineQueryResultArticle(
                id="today_first",
                title=matching_groups[0] + " 1 підгрупа",
                description="Розклад на сьогодні🌇",
                input_message_content=InputTextMessageContent(message_text=await send_lessons(
                    user_info={'group': groups_ids[matching_groups[0]], 'subgroup': "1"},
                    day=cur_day(),
                    week=cur_week()
                ))
            ),
            InlineQueryResultArticle(
                id="tomorrow_first",
                title=matching_groups[0] + " 1 підгрупа",
                description="Розклад на завтра🏙",
                input_message_content=InputTextMessageContent(message_text=await send_lessons(
                    user_info={'group': groups_ids[matching_groups[0]], 'subgroup': "1"},
                    day=cur_day()+1,
                    week=cur_week()
                ))
            ),
            InlineQueryResultArticle(
                id="today_second",
                title=matching_groups[0] + " 2 підгрупа",
                description="Розклад на сьогодні🌇",
                input_message_content=InputTextMessageContent(message_text=await send_lessons(
                    user_info={'group': groups_ids[matching_groups[0]], 'subgroup': "2"},
                    day=cur_day(),
                    week=cur_week()
                ))
            ),
            InlineQueryResultArticle(
                id="tomorrow_second",
                title=matching_groups[0] + " 2 підгрупа",
                description="Розклад на завтра🏙",
                input_message_content=InputTextMessageContent(message_text=await send_lessons(
                    user_info={'group': groups_ids[matching_groups[0]], 'subgroup': "2"},
                    day=cur_day()+1,
                    week=cur_week()
                ))
            )
        ]
        await inline_query.answer(answer, cache_time=1)
