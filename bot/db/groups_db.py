from sqlalchemy import Column, Integer, VARCHAR, DATE
import datetime

from .base import BaseModel


class Group(BaseModel):
    __tablename__ = "groups_data"

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    # Group and subgroup
    group = Column(VARCHAR(32), unique=False, nullable=False)
    subgroup = Column(VARCHAR(32), unique=False, nullable=False)

    # Reg Date
    reg_date = Column(DATE, default=datetime.date.today())

    # Маг функ
    def __str__(self) -> str:
        return f"<User:{self.user_id}>"


class Visited(BaseModel):
    __tablename__ = "visits_data"

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    # Reg Date
    reg_date = Column(DATE, default=datetime.date.today())
    # this is how to add column that not nullable with def value (server_default)
    # rand = Column(Integer, server_default="3", default=3, nullable=False)

    # Маг функ
    def __str__(self) -> str:
        return f"<User:{self.user_id}>"
