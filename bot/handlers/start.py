from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.phrases import groups, subgroups, days
from bot.phrases import start_phrases
from bot.Groups_func import send_lessons
from bot.middlewares import StartMessageMiddleware
from bot.keyboards import groups_kb, subgroups_kb, days_kb


class ChoseGroup(StatesGroup):
    choosing_group = State()
    choosing_subgroup = State()
    choosing_day = State()


start_router = Router(name='start')
start_router.message.middleware(StartMessageMiddleware())


@start_router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext, user_info: dict) -> None:
    if user_info:
        await state.update_data(group=user_info['group'], subgroup=user_info['subgroup'])
        await message.answer(
            text=start_phrases["choosing_reg"],
            reply_markup=days_kb(days)
        )
        await state.set_state(ChoseGroup.choosing_day)
    else:
        await message.answer(text=start_phrases["choosing_not_reg"].format(n=message.from_user.first_name),
                             reply_markup=groups_kb(groups))
        await state.set_state(ChoseGroup.choosing_group)


@start_router.message(
    ChoseGroup.choosing_group,
    F.text.in_(groups)
)
async def group_chosen(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await message.answer(
        text=start_phrases["choose_subgroup"],
        reply_markup=subgroups_kb(subgroups)
    )
    await state.set_state(ChoseGroup.choosing_subgroup)

# INCORRECT GROUP


@start_router.message(ChoseGroup.choosing_group)
async def group_chosen_incorrectly(message: Message):
    await message.answer(
        text=start_phrases["wrong_group"],
        reply_markup=groups_kb(groups)
    )


@start_router.message(
    ChoseGroup.choosing_subgroup,
    F.text.in_(subgroups)
)
async def subgroup_chosen(message: Message, state: FSMContext):
    await state.update_data(subgroup=message.text)
    await message.answer(
        text=start_phrases["choose_day"],
        reply_markup=days_kb(days)
    )
    await state.set_state(ChoseGroup.choosing_day)

# INCORRECT SUBGROUP


@start_router.message(ChoseGroup.choosing_subgroup)
async def subgroup_chosen_incorrectly(message: Message):
    await message.answer(
        text=start_phrases["wrong_subgroup"],
        reply_markup=groups_kb(subgroups)
    )


@start_router.message(
    ChoseGroup.choosing_day,
    F.text.in_(days)
)
async def days_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=send_lessons(user_data, days.index(message.text)+1),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

# INCORRECT DAY


@start_router.message(ChoseGroup.choosing_day)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text=start_phrases["wrong_day"],
        reply_markup=groups_kb(days)
    )
