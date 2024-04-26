from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard(reg: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оновити" if reg else "Зареєструватись",
                    callback_data="reg_or_upd",
                )
            ]
        ]
    )


def subgroups_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 підгрупа", callback_data="1")],
            [InlineKeyboardButton(text="2 підгрупа", callback_data="2")],
            [InlineKeyboardButton(text="Без підгруп", callback_data="0")],
        ]
    )
