from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    """States group for registration."""

    group = State()
    subgroup = State()


class MailingState(StatesGroup):
    """States group for mailing (admin function)"""

    text = State()
    confirmation = State()
