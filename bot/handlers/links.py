from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.middlewares import LinksMessageMiddleware
from bot.db.db_functions import (add_link_to_lesson, remove_link_to_lesson, get_links_list,
                                 check_lesson_name, check_teacher_name)
from bot.phrases import links_phrases, lesson_types


class SetLink(StatesGroup):
    sending_lesson = State()
    sending_lesson_type = State()
    sending_teacher_short_name = State()
    sending_link = State()


class RemoveLink(StatesGroup):
    lesson_to_remove = State()
    lesson_type_to_remove = State()
    lesson_teacher_to_remove = State()


links_router = Router(name='links')
links_router.message.middleware(LinksMessageMiddleware())


@links_router.message(Command("set_link"))
async def command_mailing_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text=links_phrases['waiting_lesson_name'])
    await state.set_state(SetLink.sending_lesson)


@links_router.message(SetLink.sending_lesson)
async def lesson_taker(message: Message, state: FSMContext, session_maker):

    lesson_name = message.text
    if await check_lesson_name(session_maker=session_maker, lesson_name=lesson_name):
        await message.answer(text=links_phrases['waiting_lesson_type'])
        await state.update_data(lesson_name=lesson_name)
        await state.set_state(SetLink.sending_lesson_type)
    else:
        await message.answer(text=links_phrases['wrong_lesson'])

@links_router.message(SetLink.sending_lesson_type)
async def lesson_taker(message: Message, state: FSMContext):

    lesson_type = message.text.upper()

    if lesson_type in lesson_types:
        await message.answer(text=links_phrases['waiting_teachers_name'])
        await state.update_data(lesson_type=lesson_type.upper())
        await state.set_state(SetLink.sending_teacher_short_name)
    else:
        await message.answer(text=links_phrases['wrong_type'])


@links_router.message(SetLink.sending_teacher_short_name)
async def lesson_taker(message: Message, state: FSMContext, session_maker):

    teacher_short_name = message.text

    if teacher_short_name[-1] == ".":
        if await check_teacher_name(session_maker=session_maker, teacher_short_name=teacher_short_name):
            await message.answer(text=links_phrases['waiting_link'])
            await state.update_data(teacher_short_name=teacher_short_name)
            await state.set_state(SetLink.sending_link)
        else:
            await message.answer(text=links_phrases['wrong_teacher'])
    else:
        await message.answer(text=links_phrases['no_dot'])


@links_router.message(SetLink.sending_link)
async def sending_link(message: Message, state: FSMContext, session_maker, president_group) -> None:
    data = await state.get_data()
    lesson_name = data['lesson_name']
    lesson_type = data['lesson_type']
    teacher_short_name = data['teacher_short_name']

    links = message.entities

    if links:
        for el in links:
            if el.type == 'url':
                link = el.extract_from(message.text)
                await add_link_to_lesson(session_maker,
                                         group_id=president_group,
                                         lesson_name=lesson_name,
                                         lesson_type=lesson_type,
                                         teacher_short_name=teacher_short_name,
                                         lesson_link=link)
                await message.answer(text=links_phrases['added_link'].format(n=lesson_name,
                                                                             type=lesson_type,
                                                                             teacher=teacher_short_name,
                                                                             l=message.text))
                await state.clear()
                return

    await message.answer(text=links_phrases['link_only'])


@links_router.message(Command("delete_link"))
async def link_remove(message: Message, state: FSMContext):
    await message.answer(text=links_phrases['delete_name'])
    await state.set_state(RemoveLink.lesson_to_remove)


@links_router.message(RemoveLink.lesson_to_remove)
async def link_remove(message: Message, state: FSMContext):

    lesson_name = message.text

    await message.answer(text=links_phrases['waiting_lesson_type'])
    await state.update_data(lesson_name=lesson_name)
    await state.set_state(RemoveLink.lesson_type_to_remove)


@links_router.message(RemoveLink.lesson_type_to_remove)
async def link_remove(message: Message, state: FSMContext):

    lesson_type = message.text

    await message.answer(text=links_phrases['delete_teacher_name'])
    await state.update_data(lesson_type=lesson_type.upper())
    await state.set_state(RemoveLink.lesson_teacher_to_remove)


@links_router.message(RemoveLink.lesson_teacher_to_remove)
async def link_remove(message: Message, state: FSMContext, session_maker, president_group):
    data = await state.get_data()
    lesson_name = data['lesson_name']
    lesson_type = data['lesson_type']
    teacher_short_name = message.text

    await remove_link_to_lesson(session_maker,
                                group_id=president_group,
                                lesson_name=lesson_name,
                                lesson_type=lesson_type,
                                teacher_short_name=teacher_short_name)
    await message.answer(text=links_phrases['deleted'].format(n=lesson_name,
                                                              type=lesson_type,
                                                              teacher=teacher_short_name))
    await state.clear()


@links_router.message(Command("links"))
async def get_links_list_command(message: Message, session_maker, president_group):
    await message.answer(text=links_phrases['all_links'])

    links_list = await get_links_list(session_maker, president_group)

    if links_list:
        for link in links_list:
            await message.answer(text=links_phrases['link_temp'].format(n=link[0],
                                                                        type=link[1],
                                                                        teacher=link[2],
                                                                        l=link[3]))
    else:
        await message.answer(text=links_phrases['no_links'])
