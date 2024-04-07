from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Union


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    # pool_pre - debug
    # echo - console echo
    return _create_async_engine(url=url, echo=False, pool_pre_ping=True)
# connect_args={'encoding': 'utf8'}

@DeprecationWarning
async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    ...
    # async with engine.begin() as conn:
    #     await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
