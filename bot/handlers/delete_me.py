from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.db import delete_user
from bot.phrases import del_phrases

delete_me_router = Router(name='delete_me')


@delete_me_router.message(Command("delete_me"))
async def command_start_handler(message: Message, session_maker) -> None:
    if await delete_user(session_maker, message.from_user.id):
        await message.answer(text=del_phrases["sucsessful"])
    else:
        await message.answer(text=del_phrases["unsucsessful"])
