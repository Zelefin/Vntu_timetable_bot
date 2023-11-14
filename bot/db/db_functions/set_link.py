import logging

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.groups_db import LessonsLinks


async def add_link_to_lesson(session_maker: async_sessionmaker, group_id: int,
                             lesson_name: str, lesson_type: str, teacher_short_name: str, lesson_link: str) -> None:
    async with session_maker() as session:
        async with session.begin():

            # Keys here is not only group and lesson_name, but teacher and type as well
            result = await session.execute(
                select(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name)))
            link = result.one_or_none()

            if link:
                await session.execute(update(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name)).
                                      values(lesson_link=lesson_link))
                await session.commit()
                return
            else:
                set_link = LessonsLinks(group_id=group_id,
                                        lesson_name=lesson_name,
                                        lesson_type=lesson_type,
                                        teacher_short_name=teacher_short_name,
                                        lesson_link=lesson_link)
                await session.merge(set_link)
                return


async def get_link(session_maker: async_sessionmaker, group_id: int, lesson_name: str, lesson_type: str,
                   teacher_short_name: str) -> str:
    async with session_maker() as session:
        async with session.begin():

            result = await session.execute(select(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name)))
            
            link = result.one_or_none()

            if link:
                return link[0].lesson_link
            else:
                return "Посилання не надано."


async def remove_link_to_lesson(session_maker: async_sessionmaker, group_id: int,
                                lesson_name: str, lesson_type: str, teacher_short_name: str) -> bool:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            try:
                await session.execute(delete(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name)))
                return True
            except Exception as e:
                logging.info(e)
                return False


async def get_links_list(session_maker: async_sessionmaker, group_id: int) -> list:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            groups_links = await session.execute(select(LessonsLinks).where(LessonsLinks.group_id == group_id))
            links_list = groups_links.fetchall()

            clear_links_list = []
            if links_list:
                for link in links_list:
                    clear_links_list.append([link[0].lesson_name,
                                             link[0].lesson_type,
                                             link[0].teacher_short_name,
                                             link[0].lesson_link])

            return clear_links_list
