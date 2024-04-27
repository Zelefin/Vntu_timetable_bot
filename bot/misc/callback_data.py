from aiogram.filters.callback_data import CallbackData


class InlineCallbackFactory(CallbackData, prefix="inline"):
    day: int = 0
    week: str
