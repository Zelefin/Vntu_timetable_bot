import asyncio
import datetime
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.Groups_func import get_new_cookies
from bot.handlers import routers
from bot.phrases import bot_commands
from bot.db import create_async_engine, get_session_maker
from bot.phrases import admin_id
from ScrapItUp import scrapitup_main, main_parsing_to_db
from bot.scheduled_lesson_reminder import remind_collector


async def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    await bot.set_my_commands(commands=commands_for_bot)

    postgres_url = URL.create(
        drivername="postgresql+asyncpg",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB")
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    # Alembic do this shi
    # await proceed_schemas(async_engine, BaseModel.metadata)
    # Scheduler for updating timetable
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
    scheduler.add_job(scheduled_update, trigger='cron', hour=3, minute=0, start_date=datetime.now(),
                      kwargs={"bot": bot, "session_maker": session_maker})
    scheduler.add_job(scheduled_update, trigger='cron', hour=5, minute=0, start_date=datetime.now(),
                      kwargs={"bot": bot, "session_maker": session_maker})
    scheduler.add_job(remind_collector, trigger='interval', seconds=60,
                      kwargs={"bot": bot, "session_maker": session_maker})
    scheduler.start()
    await get_new_cookies()

    # Видалимо усі вхідні месседжи
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)


async def scheduled_update(bot: Bot, session_maker: async_sessionmaker):
    try:
        await scrapitup_main()
        await bot.send_message(chat_id=admin_id, text="Txt files updated.")
        await main_parsing_to_db(session_maker)
        await bot.send_message(chat_id=admin_id, text="Timetable successfully updated!")
    except Exception as e:
        logging.info(e)
        await bot.send_message(chat_id=admin_id, text=f"Some troubles... Exception:\n\n{e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')
