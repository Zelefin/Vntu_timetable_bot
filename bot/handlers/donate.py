from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message

from bot.phrases import donate_phrases

donate_router = Router(name='donate_router')


@donate_router.message(Command("donate"))
async def command_start_handler(message: Message) -> None:
    buttons = [
        [InlineKeyboardButton(text=donate_phrases['jar'], url=donate_phrases['link'])]
    ]
    donate_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text=donate_phrases['thanks'], reply_markup=donate_keyboard)
