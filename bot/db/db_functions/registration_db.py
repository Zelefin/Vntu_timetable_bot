import logging

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import delete, select, update, true
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.groups_db import Student


async def check_user(session_maker: async_sessionmaker, uid: int) -> dict | None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(Student).where(Student.user_id == uid))
            user = result.one_or_none()

            if user:
                return {'group': user[0].group, 'subgroup': user[0].subgroup,
                        'notify': user[0].notify, 'jetiq': user[0].jetiq}
            else:
                return


async def add_user(session_maker: async_sessionmaker, uid: int, group: int, subgroup: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            result = await session.execute(select(Student).where(Student.user_id == uid))
            user = result.one_or_none()

            if user:
                return False
            else:

                user = Student(
                    user_id=uid,
                    group=group,
                    subgroup=subgroup
                )
                await session.merge(user)

                return True


async def delete_user(session_maker: async_sessionmaker, uid: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            try:
                await session.execute(delete(Student).where(Student.user_id == uid))
                return True
            except Exception as e:
                logging.info(e)
                return False


async def notify_user(session_maker: async_sessionmaker, uid: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            result = await session.execute(select(Student).where(Student.user_id == uid))
            user = result.one_or_none()

            if user:
                await session.execute(update(Student).where(Student.user_id == uid).values(notify=not user[0].notify))
                await session.commit()
                return True
            else:
                return False


async def get_users_to_notify(session_maker: async_sessionmaker,
                              group_id: int, subgroup: int) -> list:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            result = await session.execute(select(Student).where((Student.group == group_id) &
                                                                 (Student.subgroup == subgroup) &
                                                                 (Student.notify == true())))
            users = result.fetchall()

            if users:
                users_ids_list = []
                for user in users:
                    users_ids_list.append(user[0].user_id)
                return users_ids_list
            else:
                return []


async def jetiq_set_true(session_maker: async_sessionmaker, uid: int) -> None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            result = await session.execute(select(Student).where(Student.user_id == uid))
            user = result.one_or_none()

            if user:
                await session.execute(update(Student).where(Student.user_id == uid).values(jetiq=true()))
                await session.commit()
