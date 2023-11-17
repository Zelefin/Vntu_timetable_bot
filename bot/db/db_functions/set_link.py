from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, delete, update
from bot.db.groups_db import LessonsLinks


async def add_link_to_lesson(session_maker: async_sessionmaker, group_id: int,
                             lesson_name: str, lesson_type: str, teacher_short_name: str, lesson_link: str) -> None:
    async with session_maker() as session:
        async with session.begin():

            # Keys here is not only group and lesson_name, but teacher and type as well
            statement = select(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name))

            result = await session.execute(statement)
            link = result.one_or_none()

            if link:

                statement_update = update(LessonsLinks).\
                    where((LessonsLinks.group_id == group_id) &
                          (LessonsLinks.lesson_name == lesson_name) &
                          (LessonsLinks.lesson_type == lesson_type) &
                          (LessonsLinks.teacher_short_name == teacher_short_name)).\
                    values(lesson_link=lesson_link)

                await session.execute(statement_update)
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
                   teacher_short_name: str) -> tuple[str, bool]:
    async with session_maker() as session:
        async with session.begin():

            result = await session.execute(select(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name)))
            
            link = result.one_or_none()

            if link:
                return link[0].lesson_link, True
            else:
                return "Посилання не надано.", False


async def remove_link_to_lesson(session_maker: async_sessionmaker, group_id: int,
                                lesson_name: str, lesson_type: str, teacher_short_name: str) -> None:
    async with session_maker() as session:
        async with session.begin():

            statement = delete(LessonsLinks).where((LessonsLinks.group_id == group_id) &
                                           (LessonsLinks.lesson_name == lesson_name) &
                                           (LessonsLinks.lesson_type == lesson_type) &
                                           (LessonsLinks.teacher_short_name == teacher_short_name))

            await session.execute(statement)
