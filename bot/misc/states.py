from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    group = State()
    subgroup = State()
