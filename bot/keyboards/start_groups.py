from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def groups_kb(groups: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in groups:
        row = KeyboardButton(text=item)
        builder.add(row)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def subgroups_kb(subgroups: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in subgroups:
        row = KeyboardButton(text=item)
        builder.add(row)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def days_kb(days: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in days:
        row = KeyboardButton(text=item)
        builder.add(row)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
