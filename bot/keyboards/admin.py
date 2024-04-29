from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Так✅", callback_data="yes")],
            [InlineKeyboardButton(text="Ні⛔", callback_data="no")],
        ]
    )
