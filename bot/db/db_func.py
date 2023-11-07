from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from .groups_db import Group, Visited


async def check_user(session_maker: async_sessionmaker, uid: int) -> dict | None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(Group).where(Group.user_id == uid))
            user = result.one_or_none()

            if user:
                return {'group': user[0].group, 'subgroup': user[0].subgroup}
            else:
                return


async def add_user(session_maker: async_sessionmaker, uid: int, group: int, subgroup: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            result = await session.execute(select(Group).where(Group.user_id == uid))
            user = result.one_or_none()

            if user:
                return False
            else:

                user = Group(
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
                await session.execute(delete(Group).where(Group.user_id == uid))
                return True
            except Exception as e:
                print("#"*20)
                print(e)
                print("#"*20)
                return False


async def check_user_vis(session_maker: async_sessionmaker, uid: int) -> bool:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(Visited).where(Visited.user_id == uid))
            user = result.one_or_none()

            if user:
                return True
            else:
                return False


async def add_user_vis(session_maker: async_sessionmaker, uid: int) -> None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            user = Visited(user_id=uid)
            await session.merge(user)

            return


async def select_all_users(session_maker: async_sessionmaker) -> list:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            users_ids_column = await session.execute(select(Visited.user_id))
            users_list = users_ids_column.fetchall()

            return users_list


async def delete_vis_user(session_maker: async_sessionmaker, uid: int) -> None:
    async with session_maker() as session:
        async with session.begin():

            try:
                await session.execute(delete(Visited).where(Visited.user_id == uid))
                return
            except Exception as e:
                print("#"*20)
                print(e)
                print("#"*20)
                return

