from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

from bot.middlewares import DesignMessageMiddleware, DesignCallbackMiddleware
from bot.keyboards import get_design_kb, DesignCallbackFactory
from bot.days_weeks_stuff import cur_day, cur_week
from bot.Groups_func import send_lessons
from bot.phrases import design_phrases


design_router = Router(name='design')
design_router.message.middleware(DesignMessageMiddleware())
design_router.callback_query.middleware(DesignCallbackMiddleware())


@design_router.message(Command("design"))
async def command_start_handler(message: Message) -> None:
    await message.answer(text=design_phrases["just_it"], reply_markup=get_design_kb())


@design_router.callback_query(DesignCallbackFactory.filter())
async def desing_callbacks(
        callback: CallbackQuery,
        callback_data: DesignCallbackFactory,
        user_info: dict
) -> None:
    day = callback_data.day
    week = callback_data.week

    with suppress(TelegramBadRequest):
        if week == -1:
            x = 1 if cur_week() == 2 else 2
            day = 1
            await callback.message.edit_text(
                text= await send_lessons(user_info, day, x), reply_markup=get_design_kb(day, x))
            await callback.answer()
            return
        elif week == 0:
            day = cur_day()
            await callback.message.edit_text(
                text=await send_lessons(user_info, day), reply_markup=get_design_kb(day))
            await callback.answer()
            return

        if day == -1:
            day = cur_day() + 1
            if day >= 6:
                day = 1
            await callback.message.edit_text(
                text=await send_lessons(user_info, day), reply_markup=get_design_kb(day))
        elif day == 0:
            day = cur_day()
            await callback.message.edit_text(
                text=await send_lessons(user_info, day), reply_markup=get_design_kb(day))
        else:
            await callback.message.edit_text(
                text=await send_lessons(user_info, day, week), reply_markup=get_design_kb(day, week))

    await callback.answer()
