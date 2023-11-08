from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from ScrapItUp.ids_dict import groups_list
from bot.phrases import no_group


def builder_kb(kb_list: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in kb_list:
        row = KeyboardButton(text=item)
        builder.add(row)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def groups_kb(faculty: str, course: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    groups = groups_list[(faculty, course)]
    for item in groups:
        row = KeyboardButton(text=item)
        builder.add(row)
    add_group = KeyboardButton(text=no_group['not_here'])
    builder.add(add_group)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
