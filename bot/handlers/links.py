from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.middlewares import LinksMessageMiddleware
from bot.db.db_functions import add_link_to_lesson, remove_link_to_lesson, get_links_list


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
    await message.answer(text="Очікую назву предмету.\nВона має бути ідентичною як в jetiq!")
    await state.set_state(SetLink.sending_lesson)


@links_router.message(SetLink.sending_lesson)
async def lesson_taker(message: Message, state: FSMContext):

    lesson_name = message.text

    await message.answer(text="Тепер надішліть тип уроку (ЛК, ПЗ, ЛБ)")
    await state.update_data(lesson_name=lesson_name)
    await state.set_state(SetLink.sending_lesson_type)


@links_router.message(SetLink.sending_lesson_type)
async def lesson_taker(message: Message, state: FSMContext):

    lesson_type = message.text

    await message.answer(text="Тепер надішліть прізвище та ініціали викладача.\n\nНаприклад:\n\n"
                         "Кабачій В.В.\nСтахов О.Я.\nКруподьорова Л.М.\n\nТак, крапка у кінці обов'язкова.")
    await state.update_data(lesson_type=lesson_type.upper())
    await state.set_state(SetLink.sending_teacher_short_name)


@links_router.message(SetLink.sending_teacher_short_name)
async def lesson_taker(message: Message, state: FSMContext):

    teacher_short_name = message.text

    await message.answer(text="Тепер надішліть посилання")
    await state.update_data(teacher_short_name=teacher_short_name)
    await state.set_state(SetLink.sending_link)


@links_router.message(SetLink.sending_lesson)
async def lesson_taker(message: Message, state: FSMContext):

    lesson_link = message.text

    await message.answer(text="Тепер надішліть посилання")
    await state.update_data(lesson_link=lesson_link)
    await state.set_state(SetLink.sending_link)


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
                await message.answer(text=f"Тепер предмет: {lesson_name}, {lesson_type}\n\n"
                                          f"Викладача '{teacher_short_name}'\nМає посилання: {message.text}")
                await state.clear()
                return

    await message.answer(text="Я очікую посилання!")


@links_router.message(Command("delete_link"))
async def link_remove(message: Message, state: FSMContext):
    await message.answer(text="Надішліть мені назву предмету який бажаєте видалити")
    await state.set_state(RemoveLink.lesson_to_remove)


@links_router.message(RemoveLink.lesson_to_remove)
async def link_remove(message: Message, state: FSMContext):

    lesson_name = message.text

    await message.answer(text="Тепер надішліть тип уроку (ЛК, ПЗ, ЛБ)")
    await state.update_data(lesson_name=lesson_name)
    await state.set_state(RemoveLink.lesson_type_to_remove)


@links_router.message(RemoveLink.lesson_type_to_remove)
async def link_remove(message: Message, state: FSMContext):

    lesson_type = message.text

    await message.answer(text="Тепер надішліть прізвище та ініціали викладача.")
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
    await message.answer(text=f"Видалив посилання для предмету {lesson_name}, {lesson_type}"
                              f" Викладача {teacher_short_name}\n\nПеревірте це командою <i>/links</i>")
    await state.clear()


@links_router.message(Command("links"))
async def get_links_list_command(message: Message, session_maker, president_group):
    await message.answer(text="Усі уроки з посиланнями:\n\nЩоб видалити пропишіть команду /delete_link,"
                              " а потім таку ж інформацію як в повідомленні!!")

    links_list = await get_links_list(session_maker, president_group)

    if links_list:
        for link in links_list:
            await message.answer(text=f"Назва: {link[0]}\n\nТип: {link[1]}\n\nВикладач: {link[2]}\n\n"
                                      f"Посилання: {link[3]}")
    else:
        await message.answer(text="Уроків з посиланням немає")
