from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.groups_db import ClassPresidents


async def check_role(session_maker: async_sessionmaker, uid: int) -> int | None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(ClassPresidents).where(ClassPresidents.user_id == uid))
            user = result.one_or_none()

            if user:
                return user[0].group_id
            else:
                return


async def add_president(session_maker: async_sessionmaker, uid: int, group_id: int) -> None:
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession

            user = ClassPresidents(user_id=uid, group_id=group_id)
            await session.merge(user)

            return


async def select_all_presidents(session_maker: async_sessionmaker) -> list:
    async with session_maker() as session:
        async with session.begin():

            presidents_column = await session.execute(select(ClassPresidents))
            presidents_list = presidents_column.fetchall()

            clear_presidents_list = []
            if presidents_list:
                for president in presidents_list:
                    clear_presidents_list.append([president[0].user_id, president[0].group_id])

            return clear_presidents_list


async def delete_president(session_maker: async_sessionmaker, uid: int) -> None:
    async with session_maker() as session:
        async with session.begin():

            try:
                await session.execute(delete(ClassPresidents).where(ClassPresidents.user_id == uid))
                return
            except Exception as e:
                print("#" * 20)
                print(e)
                print("#" * 20)
                return

