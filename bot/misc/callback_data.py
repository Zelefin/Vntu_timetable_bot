from aiogram.filters.callback_data import CallbackData


class InlineCallbackFactory(CallbackData, prefix="inline"):
    """Callback factory for viewing timetable as message"""

    day: int = 0
    week: str
