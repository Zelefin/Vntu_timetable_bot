from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

from ScrapItUp import groups_ids
from bot.phrases import subgroups, reg_phrases, faculties, courses, no_group
from bot.db import add_user
from bot.middlewares import RegistrationMessageMiddleware
from bot.keyboards import groups_kb, builder_kb


class ChoseRegGroup(StatesGroup):
    choosing_faculty = State()
    choosing_course = State()
    choosing_group = State()
    choosing_subgroup = State()


registration_router = Router(name='reg')
registration_router.message.middleware(RegistrationMessageMiddleware())


@registration_router.message(Command("registration"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text=reg_phrases["choose_faculty"],
                         reply_markup=builder_kb(faculties))
    await state.set_state(ChoseRegGroup.choosing_faculty)


@registration_router.message(
    ChoseRegGroup.choosing_faculty,
    F.text.in_(faculties)
)
async def faculty_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_faculty=message.text)
    await message.answer(
        text=reg_phrases["choose_course"],
        reply_markup=builder_kb(courses)
    )
    await state.set_state(ChoseRegGroup.choosing_course)

# INCORRECT FACULTY


@registration_router.message(ChoseRegGroup.choosing_faculty)
async def faculty_chosen_incorrectly(message: Message):
    await message.answer(
        text=reg_phrases["incorrect_faculty"],
        reply_markup=builder_kb(faculties)
    )


@registration_router.message(
    ChoseRegGroup.choosing_course,
    F.text.in_(courses)
)
async def course_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_course=message.text)
    user_info = await state.get_data()
    await message.answer(
        text=reg_phrases["choose_group"],
        reply_markup=groups_kb(user_info['chosen_faculty'], user_info['chosen_course'])
    )
    await state.set_state(ChoseRegGroup.choosing_group)

# INCORRECT COURSE


@registration_router.message(ChoseRegGroup.choosing_course)
async def course_chosen_incorrectly(message: Message):
    await message.answer(
        text=reg_phrases["incorrect_course"],
        reply_markup=builder_kb(courses)
    )


@registration_router.message(
    ChoseRegGroup.choosing_group,
    F.text.in_(groups_ids)
)
async def group_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_group=groups_ids[message.text], chosen_group_text=message.text)
    await message.answer(
        text=reg_phrases["choose_subgroup"],
        reply_markup=builder_kb(subgroups)
    )
    await state.set_state(ChoseRegGroup.choosing_subgroup)

# INCORRECT GROUP


@registration_router.message(ChoseRegGroup.choosing_group, F.text == no_group['not_here'])
async def not_my_group(message: Message, state: FSMContext):
    await message.answer(text=no_group['answer'], reply_markup=ReplyKeyboardRemove())
    await state.clear()


@registration_router.message(ChoseRegGroup.choosing_group)
async def group_chosen_incorrectly(message: Message, state: FSMContext):
    user_info = await state.get_data()
    await message.answer(
        text=reg_phrases["incorrect_group"],
        reply_markup=groups_kb(user_info['chosen_faculty'], user_info['chosen_course'])
    )


@registration_router.message(
    ChoseRegGroup.choosing_subgroup,
    F.text.in_(subgroups)
)
async def subgroup_chosen(message: Message, state: FSMContext, session_maker):
    user_info = await state.get_data()
    chosen_group = int(user_info['chosen_group'])
    chosen_group_text = user_info['chosen_group_text']
    chosen_subgroup = int(message.text[0])

    if await add_user(session_maker, message.from_user.id, chosen_group, chosen_subgroup):
        await message.answer(
            text=reg_phrases["successful"].format(
                g=chosen_group_text, s=chosen_subgroup),
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
        reply_markup=builder_kb(subgroups)
    )
