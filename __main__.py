import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from bot.config_reader import load_config, Config
from bot.handlers import routers_list
from bot.middlewares.config import ConfigMiddleware
from bot.middlewares.database import DatabaseMiddleware
from bot.services import broadcaster
from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.vntu_timetable_api import VntuTimetableApi


async def on_startup(bot: Bot, admin_id: int):
    await broadcaster.broadcast(bot, [admin_id], "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()

    config = load_config()
    api = VntuTimetableApi()

    engine = create_engine(config)
    session_pool = create_session_pool(engine)

    storage = RedisStorage.from_url(
        config.redis.make_connection_string(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp["api"] = api
    dp["redis"] = storage.redis
    dp["bot_username"] = config.bot.username

    dp.message.filter(F.chat.type == "private")

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config, session_pool)

    await on_startup(bot, config.admin)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
