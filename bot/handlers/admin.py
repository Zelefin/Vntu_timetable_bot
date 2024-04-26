from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.filters.admin import AdminFilter
from infrastructure.vntu_timetable_api import VntuTimetableApi

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")


@admin_router.message(Command("x"))
async def admin_x(message: Message, api: VntuTimetableApi):
    print(await api.get_faculties())
    await message.answer("Didit")
