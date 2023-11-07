from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.middlewares.update_timetable_middleware import UpdateTimetableMessageMiddleware
from ScrapItUp import scrapitup_main

update_timetable_router = Router(name='delete_me')
update_timetable_router.message.middleware(UpdateTimetableMessageMiddleware())


@update_timetable_router.message(Command("update_timetable"))
async def command_start_handler(message: Message) -> None:
    try:
        scrapitup_main()
        await message.answer(text="Timetable successfully updated!")
    except Exception as e:
        print(e)
        await message.answer(text=f"Some troubles... Exception:\n\n{e}")
