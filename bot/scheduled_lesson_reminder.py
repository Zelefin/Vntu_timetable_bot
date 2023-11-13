import asyncio
from datetime import datetime, timedelta
import pytz

from aiogram import Bot

from bot.db.db_functions import get_groups_to_remind
from bot.db.db_functions import get_users_to_notify
from bot.db.db_functions import get_link
from bot.phrases import scheduled_reminder_phrases, lesson_types


async def remind_collector(bot: Bot, session_maker) -> None:
    uk_time = pytz.timezone("Europe/Kyiv")
    current_time = datetime.now(tz=uk_time)
    current_time = current_time + timedelta(minutes=5)  # На 5 хв раніше
    # Щоб видалити нуль на початку. (потрібно для збігу даних з базою)
    current_time = current_time.strftime("%H:%M").lstrip("0")
    current_day = datetime.now(tz=uk_time).strftime("%d.%m")
    result = await get_groups_to_remind(session_maker=session_maker, time=current_time, date=current_day)

    if result:
        for group in result:
            # group[0] - group_id
            # group[1] - subgroup
            # group[2] - lesson_name
            # group[3] - lesson_type
            # group[4] - teacher_short_name

            # Один урок у двох підгрупах
            if group[1] == 0:
                users1 = await get_users_to_notify(session_maker=session_maker, group_id=group[0], subgroup=1)
                users2 = await get_users_to_notify(session_maker=session_maker, group_id=group[0], subgroup=2)
                link = await get_link(session_maker=session_maker,
                                      group_id=group[0],
                                      lesson_name=group[2],
                                      lesson_type=group[3],
                                      teacher_short_name=group[4]
                                      )
                await remind_sender(bot, list(users1+users2), [group[2], group[3], group[4]], link)

            # Лише 1 підгрупа
            elif group[1] == 1:
                users = await get_users_to_notify(session_maker=session_maker, group_id=group[0], subgroup=1)
                link = await get_link(session_maker=session_maker, group_id=group[0], lesson_name=group[2])
                await remind_sender(bot, users, group[2], link)

            # Лише 2 підгрупа
            elif group[1] == 2:
                users = await get_users_to_notify(session_maker=session_maker, group_id=group[0], subgroup=2)
                link = await get_link(session_maker=session_maker, group_id=group[0], lesson_name=group[2])
                await remind_sender(bot, users, group[2], link)


async def remind_sender(bot: Bot, users_ids: list[int], lesson: list[str], link: str) -> None:
    for user_id in users_ids:
        try:
            await asyncio.sleep(0.4)
            await bot.send_message(chat_id=user_id,
                                   text=scheduled_reminder_phrases['reminder'].format(n=lesson[0],
                                                                                      type=lesson_types[lesson[1]],
                                                                                      teacher=lesson[2],
                                                                                      l=link))
        except Exception as e:
            print(e)
