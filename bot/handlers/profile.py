from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot.middlewares import DesignMessageMiddleware, DesignCallbackMiddleware
from bot.db.db_functions import notify_user
from bot.phrases import profile_phrases


profile_router = Router(name='profile')
profile_router.message.middleware(DesignMessageMiddleware())
profile_router.callback_query.middleware(DesignCallbackMiddleware())


@profile_router.message(Command("profile"))
async def command_profile_handler(message: Message, user_info) -> None:
    if user_info['notify']:
        kb = [[InlineKeyboardButton(text=profile_phrases['off'], callback_data="off")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    else:
        kb = [[InlineKeyboardButton(text=profile_phrases['on'], callback_data="on")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text=profile_phrases["profile"].format(g=user_info['group'],
                                                                s=user_info['subgroup']), reply_markup=reply_markup)


@profile_router.callback_query(F.data == "on")
async def profile_callback_on(
        callback: CallbackQuery,
        session_maker
) -> None:
    if await notify_user(session_maker=session_maker, uid=callback.from_user.id):

        kb = [[InlineKeyboardButton(text=profile_phrases['off'], callback_data="off")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        await callback.answer(text=profile_phrases['on_answ'])

    else:
        await callback.answer(text=profile_phrases['error'])


@profile_router.callback_query(F.data == "off")
async def profile_callback_off(
        callback: CallbackQuery,
        session_maker
) -> None:
    if await notify_user(session_maker=session_maker, uid=callback.from_user.id):

        kb = [[InlineKeyboardButton(text=profile_phrases['on'], callback_data="on")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

        await callback.answer(text=profile_phrases['off_answ'])

    else:
        await callback.answer(text=profile_phrases['error'])
