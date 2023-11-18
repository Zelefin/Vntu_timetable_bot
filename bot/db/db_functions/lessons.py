from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, delete, Row
from typing import Sequence

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


async def select_unique_lessons(session_maker: async_sessionmaker, group_id: int) -> Sequence[Row] | None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(Lessons.lesson_name, Lessons.lesson_type, Lessons.teacher_short_name)
                                           .where(Lessons.group_id == group_id)
                                           .group_by(Lessons.lesson_name, Lessons.lesson_type,
                                                     Lessons.teacher_short_name).order_by(Lessons.lesson_name))
            unique_lessons = result.fetchall()  # returns Sequence from typing

            return unique_lessons


async def check_lesson_name(session_maker: async_sessionmaker, lesson_name: str) -> bool:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Lessons).where((Lessons.lesson_name == lesson_name)))
            lesson = result.fetchone()

            if lesson:
                return True
            else:
                return False


async def check_teacher_name(session_maker: async_sessionmaker, teacher_short_name: str):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Lessons).where((Lessons.teacher_short_name == teacher_short_name)))
            teacher = result.fetchone()

            if teacher:
                return True
            else:
                return False


async def get_groups_to_remind(session_maker: async_sessionmaker, time: str, date: str) -> None | list:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Lessons).where((Lessons.lesson_time_start == time) &
                                                                 (Lessons.lesson_date_start == date)))

            lessons = result.fetchall()
            if lessons:
                groups_to_send = []

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
