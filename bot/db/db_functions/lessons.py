from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, delete

from bot.db.groups_db import Lessons


async def add_lesson(session_maker: async_sessionmaker,
                     group_id: int,
                     subgroup: int,
                     lesson_name: str,
                     lesson_type: str,
                     teacher_short_name: str,
                     lesson_time_start: str,
                     lesson_date_start: str) -> None:
    async with session_maker() as session:
        async with session.begin():

            lesson = Lessons(group_id=group_id,
                             subgroup=subgroup,
                             lesson_name=lesson_name,
                             lesson_type=lesson_type,
                             teacher_short_name=teacher_short_name,
                             lesson_time_start=lesson_time_start,
                             lesson_date_start=lesson_date_start)
            await session.merge(lesson)


async def get_groups_to_remind(session_maker: async_sessionmaker, time: str, date: str) -> None | list:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Lessons).where((Lessons.lesson_time_start == time) &
                                                                 (Lessons.lesson_date_start == date)))
            if result:
                groups_to_send = []
                lessons = result.fetchall()
                for lesson in lessons:
                    groups_to_send.append([lesson[0].group_id,
                                           lesson[0].subgroup,
                                           lesson[0].lesson_name,
                                           lesson[0].lesson_type,
                                           lesson[0].teacher_short_name])
                return groups_to_send
            else:
                return


async def drop_lessons_table(session_maker: async_sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            await session.execute(delete(Lessons))
