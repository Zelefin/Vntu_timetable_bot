import logging

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import bot.keyboards.user as kb
from bot.misc.states import RegistrationState
from infrastructure.database.models import User
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.vntu_timetable_api import VntuTimetableApi

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext, user: User):
    await state.clear()
    if user.faculty_id:
        await message.answer(
            text=f"Вітаю, {message.from_user.first_name}!\n\n"
            f" > Група: {user.group_name}\n"
            + (f" > Підгрупа: {user.subgroup}" if user.subgroup else ""),
            reply_markup=kb.start_keyboard(reg=True),
        )
    else:
        await message.answer(
            text=f"Вітаю, {message.from_user.first_name}!",
            reply_markup=kb.start_keyboard(reg=False),
        )


@user_router.callback_query(F.data == "reg_or_upd")
async def reg_or_upd_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="Введіть назву вашої групи:")
    await state.set_state(RegistrationState.group)


@user_router.message(RegistrationState.group)
async def handle_group_msg(message: Message, state: FSMContext, api: VntuTimetableApi):
    result, faculties = await api.get_faculties()
    if result != 200:
        await message.answer(
            "Упс... Виникла помилка при отриманні данних з API😖\nСпробуйте пізніше..."
        )
        await state.clear()
        return

    for faculty in faculties.get("data"):
        for group in faculty["groups"]:
            if group["name"].upper() == message.text.upper():
                await state.set_data(
                    {
                        "faculty_id": faculty["id"],
                        "group_id": group["id"],
                        "group_name": group["name"],
                    }
                )
                await message.answer(
                    text="Оберіть вашу підгрупу:", reply_markup=kb.subgroups_keyboard()
                )
                break

    await state.set_state(RegistrationState.subgroup)


@user_router.callback_query(RegistrationState.subgroup, F.data.in_(["0", "1", "2"]))
async def handle_subgroup_callback(
    callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot
):
    bot_info = await bot.get_me()
    data = await state.get_data()
    try:
        await repo.users.update_user_faculty_and_group(
            user_id=callback.from_user.id,
            faculty_id=data["faculty_id"],
            group_id=data["group_id"],
            group_name=data["group_name"],
            subgroup=int(callback.data),
        )
        await callback.message.edit_text(
            text="Ваші данні було успішно збережено!\n\n"
            f"Ви можете переглянути розклад для <b>{data['group_name']}</b> у "
            f"<a href='https://t.me/{bot_info.username}/timetable?startapp={data['faculty_id']}_{data['group_id']}'>web app</a>"
            f" або як повідомлення при команді <i>/inline</i>",
            reply_markup=kb.share_button(),
        )
    except Exception as e:
        logging.error(e)
        await callback.message.edit_text("Виникла помилка при збереженні данних🤕")
    await state.clear()
