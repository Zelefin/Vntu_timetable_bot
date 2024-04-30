from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.filters.admin import AdminFilter
from bot.keyboards.admin import yes_no_keyboard
from bot.misc.states import MailingState
from bot.services import broadcaster
from infrastructure.database.repo.requests import RequestsRepo

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")


@admin_router.message(Command("mailing"))
async def mailing(message: Message, state: FSMContext):
    await message.answer("Уведіть текст для розсилки")
    await state.set_state(MailingState.text)


@admin_router.message(MailingState.text)
async def text_for_mailing(message: Message, state: FSMContext):
    await message.answer(text=message.html_text)
    await message.answer(
        text="👆Я розішлю усім це повідомлення", reply_markup=yes_no_keyboard()
    )
    await state.set_data({"text": message.html_text})
    await state.set_state(MailingState.confirmation)


@admin_router.callback_query(MailingState.confirmation, F.data.in_(["yes", "no"]))
async def yes_no_mailing(
    callback: CallbackQuery, state: FSMContext, repo: RequestsRepo, bot: Bot
):
    if callback.data == "yes":
        data = await state.get_data()
        await callback.message.edit_text("Розсилку розпочато!")
        count = await broadcaster.broadcast(
            bot=bot,
            users=await repo.users.all_users_ids(),
            text=data["text"],
            repo=repo,
        )
        await callback.message.answer(text=f"Успішно розіслано: {count} юзерам")
    else:
        await callback.message.edit_text("Нічого не розсилаю")
        await state.clear()
    await callback.answer()
