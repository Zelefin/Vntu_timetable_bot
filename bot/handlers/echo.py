from aiogram import Router
from aiogram.types import CallbackQuery

echo_router = Router()


@echo_router.callback_query()
async def answer_query(callback: CallbackQuery):
    await callback.answer(show_alert=True, text="Стара версія бота!")
