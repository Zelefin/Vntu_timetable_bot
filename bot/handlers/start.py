from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

from ScrapItUp import groups_ids
from bot.phrases import subgroups, days, faculties, courses, no_group
from bot.phrases import start_phrases
from bot.Groups_func import send_lessons
from bot.middlewares import StartMessageMiddleware
from bot.keyboards import groups_kb, builder_kb


class ChoseGroup(StatesGroup):
    choosing_faculty = State()
    choosing_course = State()
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
            reply_markup=builder_kb(days)
        )
        await state.set_state(ChoseGroup.choosing_day)
    else:
        await message.answer(text=start_phrases["choosing_fac"].format(n=message.from_user.first_name),
                             reply_markup=builder_kb(faculties))
        await state.set_state(ChoseGroup.choosing_faculty)


@start_router.message(
    ChoseGroup.choosing_faculty,
    F.text.in_(faculties)
)
async def faculty_chosen(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)
    await message.answer(
        text=start_phrases["choosing_course"],
        reply_markup=builder_kb(courses)
    )
    await state.set_state(ChoseGroup.choosing_course)


# INCORRECT FACULTY


@start_router.message(ChoseGroup.choosing_faculty)
async def faculty_chosen_incorrectly(message: Message):
    await message.answer(
        text=start_phrases["wrong_faculty"],
        reply_markup=builder_kb(faculties)
    )


@start_router.message(
    ChoseGroup.choosing_course,
    F.text.in_(courses)
)
async def course_chosen(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    user_data = await state.get_data()
    await message.answer(
        text=start_phrases["choosing_group"],
        reply_markup=groups_kb(user_data['faculty'], user_data['course'])
    )
    await state.set_state(ChoseGroup.choosing_group)


# INCORRECT COURSE


@start_router.message(ChoseGroup.choosing_course)
async def course_chosen_incorrectly(message: Message):
    await message.answer(
        text=start_phrases["wrong_course"],
        reply_markup=builder_kb(courses)
    )


@start_router.message(
    ChoseGroup.choosing_group,
    F.text.in_(groups_ids)
)
async def group_chosen(message: Message, state: FSMContext):
    await state.update_data(group=groups_ids[message.text])
    await message.answer(
        text=start_phrases["choose_subgroup"],
        reply_markup=builder_kb(subgroups)
    )
    await state.set_state(ChoseGroup.choosing_subgroup)

# INCORRECT GROUP


@start_router.message(ChoseGroup.choosing_group, F.text == no_group['not_here'])
async def not_my_group(message: Message, state: FSMContext):
    await message.answer(text=no_group['answer'], reply_markup=ReplyKeyboardRemove())
    await state.clear()


@start_router.message(ChoseGroup.choosing_group)
async def group_chosen_incorrectly(message: Message, state: FSMContext):
    user_info = await state.get_data()
    await message.answer(
        text=start_phrases["wrong_group"],
        reply_markup=groups_kb(user_info['faculty'], user_info['course'])
    )


@start_router.message(
    ChoseGroup.choosing_subgroup,
    F.text.in_(subgroups)
)
async def subgroup_chosen(message: Message, state: FSMContext):
    await state.update_data(subgroup=message.text[0])
    await message.answer(
        text=start_phrases["choose_day"],
        reply_markup=builder_kb(days)
    )
    await state.set_state(ChoseGroup.choosing_day)

# INCORRECT SUBGROUP


@start_router.message(ChoseGroup.choosing_subgroup)
async def subgroup_chosen_incorrectly(message: Message):
    await message.answer(
        text=start_phrases["wrong_subgroup"],
        reply_markup=builder_kb(subgroups)
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
        reply_markup=builder_kb(days)
    )
