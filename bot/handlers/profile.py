from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from ScrapItUp import groups_ids
from bot.Groups_func import jetiq_check
from bot.db.db_functions.registration_db import jetiq_set_true
from bot.middlewares import DesignMessageMiddleware, DesignCallbackMiddleware
from bot.db.db_functions import notify_user
from bot.phrases import profile_phrases


profile_router = Router(name='profile')
profile_router.message.middleware(DesignMessageMiddleware())
profile_router.callback_query.middleware(DesignCallbackMiddleware())


class CheckJet(StatesGroup):
    sending_answer = State()
    sending_id = State()


@profile_router.message(Command("profile"))
async def command_profile_handler(message: Message, user_info) -> None:
    if user_info['notify']:
        kb = [[InlineKeyboardButton(text=profile_phrases['off'], callback_data="off")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    else:
        kb = [[InlineKeyboardButton(text=profile_phrases['on'], callback_data="on")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text=profile_phrases["profile"].format(g=[key for key, value in groups_ids.items()
                                                                   if value == str(user_info['group'])][0],
                                                                s=user_info['subgroup']), reply_markup=reply_markup)


@profile_router.callback_query(F.data == "on")
async def profile_callback_on(
        callback: CallbackQuery,
        session_maker,
        user_info,
        bot: Bot,
        state: FSMContext
) -> None:
    if user_info['jetiq']:
        if await notify_user(session_maker=session_maker, uid=callback.from_user.id):

            kb = [[InlineKeyboardButton(text=profile_phrases['off'], callback_data="off")]]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
            await callback.message.edit_reply_markup(reply_markup=reply_markup)

            await callback.answer(text=profile_phrases['on_answ'])

        else:
            await callback.answer(text=profile_phrases['error'])
    else:
        kb = [[InlineKeyboardButton(text=profile_phrases['begin_check'], callback_data="begin")],
              [InlineKeyboardButton(text=profile_phrases['cancel_check'], callback_data="stop")]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback.message.delete()
        msg: list[Message] = await bot.send_media_group(chat_id=callback.from_user.id, media=[
            InputMediaPhoto(media=profile_phrases['first_photo'])
            , InputMediaPhoto(media=profile_phrases['second_photo'])
        ])
        msg2 = await bot.send_message(chat_id=callback.from_user.id, text=profile_phrases['on_check'],
                                      reply_markup=reply_markup)
        await state.set_state(CheckJet.sending_answer)
        await state.update_data(msg0=msg[0].message_id, msg1=msg[1].message_id, msg2=msg2.message_id)

    await callback.answer()


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

    await callback.answer()


@profile_router.callback_query(F.data == "stop", CheckJet.sending_answer)
async def profile_callback_off(
        callback: CallbackQuery,
        state: FSMContext,
        bot: Bot
) -> None:

    data = await state.get_data()

    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['msg0'])
    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['msg1'])
    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['msg2'])

    await callback.message.answer(text=profile_phrases['cancel_ok'])
    await state.clear()

    await callback.answer()


@profile_router.callback_query(F.data == "begin", CheckJet.sending_answer)
async def profile_callback_off(
        callback: CallbackQuery,
        state: FSMContext,
        bot: Bot
) -> None:

    data = await state.get_data()

    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['msg0'])
    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['msg1'])
    await bot.delete_message(chat_id=callback.from_user.id, message_id=data['msg2'])

    await callback.message.answer(text=profile_phrases['begin_wait'])
    await state.set_state(CheckJet.sending_id)

    await callback.answer()


@profile_router.message(CheckJet.sending_id)
async def profile_callback_off(
        message: Message,
        session_maker,
        state: FSMContext
) -> None:

    jetid = message.text

    if await jetiq_check(jetid):
        await message.answer(text=profile_phrases['check_ok'])
        await jetiq_set_true(session_maker, message.from_user.id)
        await notify_user(session_maker=session_maker, uid=message.from_user.id)
    else:
        await message.answer(text=profile_phrases['check_failed'])

    await state.clear()
