from typing import Optional
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from bot.days_weeks_stuff import cur_week

days_short = ["🔴", "Пн", "Вт", "Ср", "Чт", "Пт"]


class DesignCallbackFactory(CallbackData, prefix="design"):
    day: Optional[int] = None
    week: Optional[int] = None


def get_design_kb(chosen_day: int = 0, w: int = None) -> InlineKeyboardMarkup:
    # TODO: maybe this is not the best idea
    w = w if w is not None else cur_week()

    builder = InlineKeyboardBuilder()
    # Here is simple function to replace button text if it's pressed
    def check_number(num, target): return 0 if num == target else num

    builder.button(
        text=days_short[check_number(
            1, chosen_day)], callback_data=DesignCallbackFactory(day=1, week=w)
    ),
    builder.button(
        text=days_short[check_number(
            2, chosen_day)], callback_data=DesignCallbackFactory(day=2, week=w)
    ),
    builder.button(
        text=days_short[check_number(
            3, chosen_day)], callback_data=DesignCallbackFactory(day=3, week=w)
    ),
    builder.button(
        text=days_short[check_number(
            4, chosen_day)], callback_data=DesignCallbackFactory(day=4, week=w)
    ),
    builder.button(
        text=days_short[check_number(
            5, chosen_day)], callback_data=DesignCallbackFactory(day=5, week=w)
    )

    builder.button(
        text="Сьогодні🌇", callback_data=DesignCallbackFactory(day=0)
    ),
    builder.button(
        text="Завтра🏙", callback_data=DesignCallbackFactory(day=-1)
    )

    if w != cur_week():
        builder.button(
            text="⬇️Цей тиждень", callback_data=DesignCallbackFactory(week=0)
        )
    else:
        builder.button(
            text="➡️Наступний тиждень", callback_data=DesignCallbackFactory(week=-1)
        )

    builder.adjust(5, 2, 1)

    return builder.as_markup()
