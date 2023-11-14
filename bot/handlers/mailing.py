import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.middlewares import MailingMessageMiddleware
from bot.db.db_functions import delete_user, delete_vis_user


class SendMail(StatesGroup):
    sending_message = State()
    confirm_sending = State()


mailing_router = Router(name='mailing')
mailing_router.message.middleware(MailingMessageMiddleware())


@mailing_router.message(Command("mailing"))
async def command_mailing_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Очікую повідомлення для розсилки...")
    await state.set_state(SendMail.sending_message)


@mailing_router.message(SendMail.sending_message)
async def message_taker(message: Message, state: FSMContext):

    message_to_be_send = message.html_text

    await message.answer("Я відправлю таке повідомлення:")
    await message.answer(text=message_to_be_send)

    await message.answer("Підтвердіть:\n(Так/Ні)")
    await state.update_data(message_to_be_send=message_to_be_send)
    await state.set_state(SendMail.confirm_sending)


@mailing_router.message(
    SendMail.confirm_sending,
    F.text == "Так"
)
async def sending_on(message: Message, state: FSMContext, bot: Bot, users_ids: list, session_maker):
    data = await state.get_data()
    message_send = data['message_to_be_send']

    users_who_got_it = 0

    for user_id in users_ids:
        try:
            await bot.send_message(chat_id=user_id[0], text=message_send)
            await asyncio.sleep(0.5)
            users_who_got_it += 1
        except Exception as e:
            logging.info(e)
            await delete_user(session_maker=session_maker, uid=user_id[0])
            await delete_vis_user(session_maker=session_maker, uid=user_id[0])

    await message.answer(text=f"Users who got message {users_who_got_it}/{len(users_ids)}")

    await state.clear()


@mailing_router.message(
    SendMail.confirm_sending,
    F.text == "Ні"
)
async def sending_off(message: Message, state: FSMContext):
    await message.answer(text="Нічого не відправляю")
    await state.clear()


@mailing_router.message(Command("users"))
async def command_all_users(message: Message, users_ids: list) -> None:
    await message.answer(text=f"Total amount of users: {len(users_ids)}")
