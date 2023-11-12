from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.middlewares import MailingMessageMiddleware
from bot.db.db_functions import add_president, check_user, delete_president, select_all_presidents


class AddPresident(StatesGroup):
    sending_id = State()


class RemovePresident(StatesGroup):
    sending_id = State()


presidents_router = Router(name='presidents')
presidents_router.message.middleware(MailingMessageMiddleware())  # we just need to check if it's admin


@presidents_router.message(Command("add_president"))
async def command_add_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Gimme id of the user")
    await state.set_state(AddPresident.sending_id)


@presidents_router.message(AddPresident.sending_id)
async def adding_president(message: Message, state: FSMContext, session_maker):

    presidents_id = int(message.text)
    result = await check_user(session_maker=session_maker, uid=presidents_id)

    if result:
        await add_president(session_maker=session_maker, uid=presidents_id, group_id=result['group'])
        await message.answer(text="User successfully promoted")
    else:
        await message.answer(text="I don't think he's registered")

    await state.clear()


@presidents_router.message(Command("remove_president"))
async def remove_president(message: Message, state: FSMContext):
    await message.answer(text="Gimme id of president")
    await state.set_state(RemovePresident.sending_id)


@presidents_router.message(RemovePresident.sending_id)
async def id_to_remove_president(message: Message, state: FSMContext, session_maker):

    await delete_president(session_maker, uid=int(message.text))
    await message.answer(text=f"User rights revoked")
    await state.clear()

@presidents_router.message(Command("presidents"))
async def get_links_list_command(message: Message, session_maker):
    await message.answer(text="Presidents list\n\nID | Group_id")

    presidents_list = await select_all_presidents(session_maker)

    if presidents_list:
        for president in presidents_list:
            await message.answer(text=f"ID: {president[0]}\n\nGroup_id: {president[1]}")
    else:
        await message.answer(text="No presidents")
