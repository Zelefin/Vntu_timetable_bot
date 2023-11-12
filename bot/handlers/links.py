from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.middlewares import LinksMessageMiddleware
from bot.db.db_functions import add_link_to_lesson, remove_link_to_lesson, get_links_list


class SetLink(StatesGroup):
    sending_lesson = State()
    sending_link = State()


class RemoveLink(StatesGroup):
    link_to_remove = State()


links_router = Router(name='links')
links_router.message.middleware(LinksMessageMiddleware())


@links_router.message(Command("set_link"))
async def command_mailing_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Очікую назву предмету.\nВона має бути ідентичною як в jetiq!")
    await state.set_state(SetLink.sending_lesson)


@links_router.message(SetLink.sending_lesson)
async def lesson_taker(message: Message, state: FSMContext):

    lesson_name = message.text

    await message.answer("Тепер надішліть посилання")
    await state.update_data(lesson_name=lesson_name)
    await state.set_state(SetLink.sending_link)


@links_router.message(SetLink.sending_link)
async def sending_link(message: Message, state: FSMContext, session_maker, president_group) -> None:
    data = await state.get_data()
    lesson_name = data['lesson_name']

    links = message.entities

    if links:
        for el in links:
            if el.type == 'url':
                link = el.extract_from(message.text)
                await add_link_to_lesson(session_maker, group_id=president_group, lesson_name=lesson_name,
                                         lesson_link=link)
                await message.answer(text=f"Тепер предмет {lesson_name} має посилання: {message.text}")
                await state.clear()
                return

    await message.answer(text="Я очікую посилання!")


@links_router.message(Command("delete_link"))
async def link_remove(message: Message, state: FSMContext):
    await message.answer(text="Надішліть мені назву предмету який бажаєте видалити")
    await state.set_state(RemoveLink.link_to_remove)


@links_router.message(RemoveLink.link_to_remove)
async def link_to_remove_got(message: Message, state: FSMContext, session_maker, president_group):

    await remove_link_to_lesson(session_maker, group_id=president_group, lesson_name=message.text)
    await message.answer(text=f"Видалив посилання для предмету {message.text}")
    await state.clear()


@links_router.message(Command("links"))
async def get_links_list_command(message: Message, session_maker, president_group):
    await message.answer(text="Усі уроки з посиланнями:\nЩоб видалити пропишіть команду /delete_link,"
                              " а потім таку ж назву як у повідомлені!!")

    links_list = await get_links_list(session_maker, president_group)

    if links_list:
        for link in links_list:
            await message.answer(text=f"Назва: {link[0]}\n\nПосилання: {link[1]}")
    else:
        await message.answer(text="Уроків з посиланням немає")
