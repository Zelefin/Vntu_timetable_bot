from contextlib import suppress

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import Row
from typing import Sequence

from bot.keyboards import dynamic_links, LinksCallbackFactory
from bot.middlewares import LinksMessageMiddleware
from bot.db.db_functions import select_unique_lessons, get_link, add_link_to_lesson, remove_link_to_lesson
from bot.phrases import links_phrases, lesson_types


class SetLink(StatesGroup):
    sending_link = State()


links_router = Router(name='links')
links_router.message.middleware(LinksMessageMiddleware())
links_router.callback_query.middleware(LinksMessageMiddleware())


@links_router.message(Command("links"))
async def get_links_list_command(message: Message, session_maker, president_group: int):

    lessons_list: Sequence[Row] | None = await select_unique_lessons(session_maker, president_group)

    if lessons_list:
        lesson_name = lessons_list[0][0]
        lesson_type = lessons_list[0][1]
        lesson_teacher = lessons_list[0][2]

        link = await get_link(session_maker,
                              group_id=president_group,
                              lesson_name=lesson_name,
                              lesson_type=lesson_type,
                              teacher_short_name=lesson_teacher)

        await message.answer(text=links_phrases['link_temp'].format(n=lesson_name,
                                                                    type=lesson_types[lesson_type],
                                                                    teacher=lesson_teacher,
                                                                    l=link[0]),
                             reply_markup=dynamic_links(lessons_list, has_link=link[1]))
    else:
        await message.answer(text=links_phrases['no_lessons'])


@links_router.callback_query(LinksCallbackFactory.filter())
async def links_callbacks(
        callback: CallbackQuery,
        session_maker,
        president_group: int,
        callback_data: LinksCallbackFactory,
        state: FSMContext
) -> None:
    lessons_list: Sequence[Row] = await select_unique_lessons(session_maker, president_group)

    action: str = callback_data.action
    position: int = callback_data.position

    with suppress(TelegramBadRequest):
        if action == "next":
            lesson_name = lessons_list[position - 1][0]
            lesson_type = lessons_list[position - 1][1]
            lesson_teacher = lessons_list[position - 1][2]

            link = await get_link(session_maker,
                                  group_id=president_group,
                                  lesson_name=lesson_name,
                                  lesson_type=lesson_type,
                                  teacher_short_name=lesson_teacher)

            await callback.message.edit_text(
                text=links_phrases['link_temp'].format(
                    n=lesson_name,
                    type=lesson_types[lesson_type],
                    teacher=lesson_teacher,
                    l=link[0]),
                reply_markup=dynamic_links(lessons_list, has_link=link[1], position=position)
            )
        elif action == "prev":
            lesson_name = lessons_list[position][0]
            lesson_type = lessons_list[position][1]
            lesson_teacher = lessons_list[position][2]

            link = await get_link(session_maker,
                                  group_id=president_group,
                                  lesson_name=lesson_name,
                                  lesson_type=lesson_type,
                                  teacher_short_name=lesson_teacher)

            await callback.message.edit_text(
                text=links_phrases['link_temp'].format(n=lesson_name,
                                                       type=lesson_types[lesson_type],
                                                       teacher=lesson_teacher,
                                                       l=link[0]),
                reply_markup=dynamic_links(lessons_list, has_link=link[1], position=position))

        elif action == "add_link":
            msg = await callback.message.answer(text=links_phrases['waiting_link'])
            await state.set_state(SetLink.sending_link)
            await state.update_data(lesson=lessons_list[position - 1], msg=msg.message_id)

        elif action == "remove_link":
            await remove_link_to_lesson(session_maker=session_maker,
                                        group_id=president_group,
                                        lesson_name=lessons_list[position - 1][0],
                                        lesson_type=lessons_list[position - 1][1],
                                        teacher_short_name=lessons_list[position - 1][2])

            await callback.message.edit_text(
                text=links_phrases['link_temp'].format(n=lessons_list[position - 1][0],
                                                       type=lesson_types[lessons_list[position - 1][1]],
                                                       teacher=lessons_list[position - 1][2],
                                                       l="<b>Видалено!</b>"),
                reply_markup=dynamic_links(lessons_list, has_link=False, position=position)
            )

    await callback.answer()


@links_router.message(SetLink.sending_link)
async def set_link(message: Message, state: FSMContext, bot: Bot, session_maker, president_group) -> None:

    data = await state.get_data()
    lesson = data['lesson']
    msg = data['msg']
    links = message.entities

    if links:
        for el in links:
            if el.type == 'url':
                link = el.extract_from(message.text)
                await add_link_to_lesson(session_maker,
                                         group_id=president_group,
                                         lesson_name=lesson[0],
                                         lesson_type=lesson[1],
                                         teacher_short_name=lesson[2],
                                         lesson_link=link
                                         )

                await state.clear()
                await message.delete()
                await bot.delete_message(chat_id=message.chat.id, message_id=msg)
                await message.answer(text="Посилання додав.")
                return

    await message.answer(text=links_phrases['link_only'])
