from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.phrases import feedback_phrases


class SendFeedback(StatesGroup):
    sending_message = State()


feedback_router = Router(name='feedback')


@feedback_router.message(Command("feedback"))
async def command_feedback_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text=feedback_phrases["on_send"])
    await state.set_state(SendFeedback.sending_message)


@feedback_router.message(SendFeedback.sending_message, Command("cancel"))
async def message_taker(message: Message, state: FSMContext):
    await message.answer(text=feedback_phrases["sending_stop"])
    await state.clear()


@feedback_router.message(
    SendFeedback.sending_message
)
async def sending_on(message: Message, state: FSMContext, bot: Bot):
    message_to_admin = message.text
    try:
        if len(message_to_admin) > 250:
            await message.answer(text=feedback_phrases["too_long"])
        else:
            await bot.send_message(chat_id=845597372, text=f"From user: {message.from_user.full_name}\n"
                                                           f"User ID: {message.from_user.id}\n"
                                                           f"Message: {message_to_admin}")  # admins ID
            await message.answer(text=feedback_phrases["good"])

    except Exception as e:
        print(e)
        await message.answer(text=feedback_phrases["bad_stuff"])

    await state.clear()
