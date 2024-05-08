from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.misc.callback_data import InlineCallbackFactory
from bot.misc.current_date import current_week

days = ["🔴", "Пн", "Вт", "Ср", "Чт", "Пт"]


def start_keyboard(reg: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оновити🔄" if reg else "Зареєструватись✍",
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


def share_button(group_name: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Поділитися", switch_inline_query=group_name)]
        ]
    )


def inline_timetable_keyboard(day: int, week: str):
    kb = InlineKeyboardBuilder()
    cur_week = current_week()
    kb.button(
        text=days[1 if day != 0 else 0],
        callback_data=InlineCallbackFactory(day=0, week=week),
    )
    kb.button(
        text=days[2 if day != 1 else 0],
        callback_data=InlineCallbackFactory(day=1, week=week),
    )
    kb.button(
        text=days[3 if day != 2 else 0],
        callback_data=InlineCallbackFactory(day=2, week=week),
    )
    kb.button(
        text=days[4 if day != 3 else 0],
        callback_data=InlineCallbackFactory(day=3, week=week),
    )
    kb.button(
        text=days[5 if day != 4 else 0],
        callback_data=InlineCallbackFactory(day=4, week=week),
    )

    kb.button(
        text="Сьогодні🌆", callback_data=InlineCallbackFactory(day=-1, week=cur_week)
    )
    kb.button(
        text="Завтра🏙", callback_data=InlineCallbackFactory(day=-2, week=cur_week)
    )

    kb.button(
        text="➡Наступний тиждень" if week == cur_week else "⬇Цей тиждень",
        callback_data=InlineCallbackFactory(
            day=day, week="firstWeek" if week == "secondWeek" else "secondWeek"
        ),
    )

    kb.adjust(5, 2, 1)
    return kb.as_markup()
