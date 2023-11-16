import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.middlewares.update_timetable_middleware import UpdateTimetableMessageMiddleware
from ScrapItUp import scrapitup_main, main_parsing_to_db

update_timetable_router = Router(name='update_timetable')
update_timetable_router.message.middleware(UpdateTimetableMessageMiddleware())


@update_timetable_router.message(Command("update_timetable"))
async def command_start_handler(message: Message, session_maker) -> None:
    try:
        await scrapitup_main()
        await message.answer(text="Txt files updated.")
        await main_parsing_to_db(session_maker=session_maker)
        await message.answer(text="Timetable successfully updated!")
    except Exception as e:
        logging.info(e)
        await message.answer(text=f"Some troubles... Exception:\n\n{e}")


@update_timetable_router.message(Command("update_txt"))
async def command_start_handler(message: Message) -> None:
    try:
        await scrapitup_main()
        await message.answer(text="Txt files updated.")
    except Exception as e:
        logging.info(e)
        await message.answer(text=f"Some troubles... Exception:\n\n{e}")


@update_timetable_router.message(Command("update_data"))
async def command_start_handler(message: Message, session_maker) -> None:
    try:
        await main_parsing_to_db(session_maker=session_maker)
        await message.answer(text="Data successfully updated!")
    except Exception as e:
        logging.info(e)
        await message.answer(text=f"Some troubles... Exception:\n\n{e}")