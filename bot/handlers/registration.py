from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.phrases import groups, subgroups, reg_phrases
from bot.db import add_user
from bot.middlewares import RegistrationMessageMiddleware
from bot.keyboards import groups_kb, subgroups_kb, days_kb


class ChoseRegGroup(StatesGroup):
    choosing_group = State()
    choosing_subgroup = State()


registration_router = Router(name='reg')
registration_router.message.middleware(RegistrationMessageMiddleware())


@registration_router.message(Command("registration"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text=reg_phrases["choose_group"],
                         reply_markup=groups_kb(groups))
    await state.set_state(ChoseRegGroup.choosing_group)


@registration_router.message(
    ChoseRegGroup.choosing_group,
    F.text.in_(groups)
)
async def group_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_group=message.text)
    await message.answer(
        text=reg_phrases["choose_subgroup"],
        reply_markup=subgroups_kb(subgroups)
    )
    await state.set_state(ChoseRegGroup.choosing_subgroup)

# INCORRECT GROUP


@registration_router.message(ChoseRegGroup.choosing_group)
async def group_chosen_incorrectly(message: Message):
    await message.answer(
        text=reg_phrases["incorrect_group"],
        reply_markup=groups_kb(groups)
    )


@registration_router.message(
    ChoseRegGroup.choosing_subgroup,
    F.text.in_(subgroups)
)
async def subgroup_chosen(message: Message, state: FSMContext, session_maker):
    chosen_group = await state.get_data()
    chosen_group = chosen_group['chosen_group']
    chosen_subgroup = message.text

    if await add_user(session_maker, message.from_user.id, chosen_group, chosen_subgroup):
        await message.answer(
            text=reg_phrases["sucsessful"].format(
                g=chosen_group, s=chosen_subgroup),
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(text=reg_phrases["failed"], reply_markup=ReplyKeyboardRemove())
    await state.clear()

# INCORRECT SUBGROUP


@registration_router.message(ChoseRegGroup.choosing_subgroup)
async def subgroup_chosen_incorrectly(message: Message):
    await message.answer(
        text=reg_phrases["incorrect_subgroup"],
        reply_markup=groups_kb(subgroups)
    )
