import json
import logging
from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from redis.asyncio import Redis

import bot.keyboards.user as kb
from bot.misc.callback_data import InlineCallbackFactory
from bot.misc.current_date import current_day, current_week
from bot.misc.states import RegistrationState
from bot.misc.timetable_message import timetable_message_generator
from infrastructure.database.models import User
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.vntu_timetable_api import VntuTimetableApi

user_router = Router()


@user_router.message(CommandStart())
async def user_start(
    message: Message, state: FSMContext, user: User, bot_username: str
):
    await state.clear()
    if user.faculty_id:
        await message.answer_photo(
            photo=(
                "AgACAgIAAxkBAAEBaCRmNTeMhHxX0QhmGYfPFo5z0FnwnQACm9wxG2zuoEmaIkh9lfC6oQEAAwIAA3gAAzQE"
                if bot_username == "vntu_timetable_bot"
                else "AgACAgIAAxkBAAI672Yz819tnBGbLe4q-4PTjGAOxSifAAKb3DEbbO6gScb8iyCe5NWTAQADAgADeAADNAQ"
            ),
            caption=f"""
Вітаю!👋
Канал з оновленнями бота: @vntu_timetable_bot_news

📲 Переглядайте розклад будь-якої групи будь-якого факультету у <b>Web App</b>.

👥 Переглядайте розклад Вашої групи (та підгрупи) як повідомлення при команді <i>/inline</i>.

ℹ️ Ваша інформація:
    > Група: <code>{user.group_name}</code>"""
            + (
                f"\n    > Підгрупа: <code>{user.subgroup} Підгрупа</code>"
                if user.subgroup
                else ""
            )
            + """

<b>Тисніть щоб оновити інформацію про себе</b>👇
            """,
            reply_markup=kb.start_keyboard(reg=True),
        )
    else:
        await message.answer_photo(
            photo=(
                "AgACAgIAAxkBAAEBaCRmNTeMhHxX0QhmGYfPFo5z0FnwnQACm9wxG2zuoEmaIkh9lfC6oQEAAwIAA3gAAzQE"
                if bot_username == "vntu_timetable_bot"
                else "AgACAgIAAxkBAAI672Yz819tnBGbLe4q-4PTjGAOxSifAAKb3DEbbO6gScb8iyCe5NWTAQADAgADeAADNAQ"
            ),
            caption="""
Вітаю!👋
Канал з оновленнями бота: @vntu_timetable_bot_news

📲 Переглядайте розклад будь-якої групи будь-якого факультету у <b>Web App</b>.

👥 Переглядайте розклад Вашої групи (та підгрупи) як повідомлення при команді <i>/inline</i>.

<b>Зареєструйтесь і отримайте доступ до усього функціоналу бота</b>👇
""",
            reply_markup=kb.start_keyboard(reg=False),
        )


@user_router.callback_query(F.data == "reg_or_upd")
async def reg_or_upd_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Введіть назву вашої групи, наприклад: <code>6ПІ-23б</code>,"
        " <code>КІВТ-23м</code>, <code>133-23a</code>"
    )
    await state.set_state(RegistrationState.group)


@user_router.message(RegistrationState.group)
async def handle_group_msg(
    message: Message, state: FSMContext, api: VntuTimetableApi, redis: Redis
):
    if faculties_redis := await redis.get("faculties"):
        faculties = json.loads(faculties_redis)
    else:
        result, faculties = await api.get_faculties()
        if result != 200 or not faculties:
            await message.answer(
                "Виникла помилка при отриманні данних з API😖\nСпробуйте пізніше..."
            )
            await state.clear()
            return
        await redis.set("faculties", json.dumps(faculties), ex=1800)

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
                await state.set_state(RegistrationState.subgroup)
                return
    else:
        await message.answer("Такої групи не знайдено. Спробуйте знову.")


@user_router.callback_query(RegistrationState.subgroup, F.data.in_(["0", "1", "2"]))
async def handle_subgroup_callback(
    callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot_username: str
):
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
            text="<i>Ваші дані було успішно збережено!</i>\n\n"
            f"Ви можете переглянути розклад для <b>{data['group_name']}</b> у "
            f"<a href='https://t.me/{bot_username}/timetable?startapp={data['faculty_id']}_{data['group_id']}'>"
            "Web App</a>"
            " або як повідомлення при команді <i>/inline</i>",
            reply_markup=kb.share_button(
                faculty_id=data["faculty_id"], group_id=data["group_id"]
            ),
        )
    except Exception as e:
        logging.error(e)
        await callback.message.edit_text("Виникла помилка при збереженні данних🤕")
    await state.clear()


@user_router.message(Command("timetable"))
async def timetable_app(message: Message, user: User, bot_username: str):
    if user.group_id and user.faculty_id:
        # It's kinda makes no sense, because we can't have faculty id w/o group id, but Pycharm will raise warning
        # Expected type 'int | str', got 'InstrumentedAttribute[_T_co]' instead (if we check only group or faculty)
        await message.answer(
            text=f"<b>Розклад для групи "
            f"<a href='https://t.me/{bot_username}/timetable?startapp={user.faculty_id}_{user.group_id}'>"
            f"{user.group_name}</a></b>",
            reply_markup=kb.share_button(
                faculty_id=user.faculty_id, group_id=user.group_id
            ),
        )
    else:
        await message.answer("Спочатку зареєструйтесь в боті командою <i>/start</i>")


@user_router.message(Command("inline"))
async def timetable_with_inline_kb(
    message: Message, api: VntuTimetableApi, user: User, redis: Redis
):
    if user.group_id and user.faculty_id:
        # Same warning even if we only use group id :/
        if current_day() > 4:
            day = 0
            week = "firstWeek" if current_week() == "secondWeek" else "secondWeek"
        else:
            day = current_day()
            week = current_week()

        timetable = await get_timetable(
            user=user, redis=redis, api=api, week=week, day=day
        )
        if not timetable:
            await message.answer(
                "Виникла помилка при отриманні данних з API😖\nСпробуйте пізніше..."
            )
            return

        await message.answer(
            text=timetable,
            reply_markup=kb.inline_timetable_keyboard(day=day, week=week),
        )
    else:
        await message.answer("Спочатку зареєструйтесь в боті командою <i>/start</i>")


@user_router.callback_query(InlineCallbackFactory.filter())
async def handle_inline_timetable_callback(
    callback: CallbackQuery,
    callback_data: InlineCallbackFactory,
    api: VntuTimetableApi,
    redis: Redis,
    user: User,
):
    day = callback_data.day
    week = callback_data.week
    match day:
        case -1:
            # today
            if current_day() > 4:
                day = 0
                week = "firstWeek" if current_week() == "secondWeek" else "secondWeek"
            else:
                day = current_day()
        case -2:
            # tomorrow
            if current_day() >= 4:
                day = 1
                week = "firstWeek" if current_week() == "secondWeek" else "secondWeek"
            else:
                day = current_day() + 1
        case _:
            pass

    with suppress(TelegramBadRequest):
        if user.group_id and user.faculty_id:
            timetable = await get_timetable(
                user=user, redis=redis, api=api, week=week, day=day
            )

            if not timetable:
                await callback.message.edit_text(
                    "Виникла помилка при отриманні данних з API😖\nСпробуйте пізніше..."
                )
                return

            await callback.message.edit_text(
                text=timetable,
                reply_markup=kb.inline_timetable_keyboard(day=day, week=week),
            )
        else:
            await callback.message.edit_text(
                text="Спочатку зареєструйтесь в боті командою <i>/start</i>"
            )

    await callback.answer()


async def get_timetable(
    user: User, redis: Redis, api: VntuTimetableApi, week: str, day: int
) -> str | None:
    if timetable_list := await redis.get(str(user.group_id) + str(user.subgroup)):
        timetable = json.loads(timetable_list)[week][day]
    else:
        status, timetable_response = await api.get_group_timetable(
            group_id=user.group_id
        )
        if status != 200 or not timetable_response:
            return
        timetable_list = timetable_message_generator(
            timetable=timetable_response,
            group_name=user.group_name,
            subgroup=user.subgroup,
        )
        await redis.set(
            str(user.group_id) + str(user.subgroup), json.dumps(timetable_list), ex=1800
        )
        timetable = timetable_list[week][day]

    return timetable
