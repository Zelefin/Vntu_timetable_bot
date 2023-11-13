from sqlalchemy import Column, Integer, DATE, BigInteger, String, Boolean, VARCHAR, false, PrimaryKeyConstraint
import datetime

from .base import BaseModel


class Group(BaseModel):
    __tablename__ = "groups_data"

    # Telegram user id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)

    # Group and subgroup
    group = Column(Integer, unique=False, nullable=False)
    subgroup = Column(Integer, unique=False, nullable=False)

    # Should we notify user that lesson has begun?
    notify = Column(Boolean, default=False, server_default=false())

    # Reg Date
    reg_date = Column(DATE, default=datetime.date.today())

    # Маг функ
    def __str__(self) -> str:
        return f"<User:{self.user_id}>"


class Visited(BaseModel):
    __tablename__ = "visits_data"

    # Telegram user id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)

    # Reg Date
    reg_date = Column(DATE, default=datetime.date.today())
    # this is how to add column that not nullable with def value (server_default)
    # rand = Column(Integer, server_default="3", default=3, nullable=False)

    # Маг функ
    def __str__(self) -> str:
        return f"<User:{self.user_id}>"


class Lessons(BaseModel):
    __tablename__ = "lessons_data"

    # Group id cant be unique, because group can have lots of lessons
    group_id = Column(Integer, unique=False, nullable=False, primary_key=True)

    # Subgroup too
    subgroup = Column(Integer, unique=False, nullable=False)

    # Lesson name
    lesson_name = Column(String, unique=False, nullable=False, primary_key=True)

    # Lesson type
    lesson_type = Column(VARCHAR(2), unique=False, nullable=False)

    # Teacher short name
    teacher_short_name = Column(String, unique=False, nullable=False)

    # When lesson starts
    lesson_time_start = Column(VARCHAR(5), unique=False, nullable=False, primary_key=True)
    lesson_date_start = Column(VARCHAR(5), unique=False, nullable=False, primary_key=True)

    # # Маг функ
    # def __str__(self) -> str:
    #     return f"<group:{self.user_id}>"


class LessonsLinks(BaseModel):
    __tablename__ = "lessons_links"

    # Group id
    group_id = Column(Integer, nullable=False, primary_key=True)

    # Name of the lesson
    lesson_name = Column(String, nullable=False, primary_key=True)

    # Lesson type
    lesson_type = Column(VARCHAR(2), unique=False, nullable=False)

    # Teacher short name
    teacher_short_name = Column(String, unique=False, nullable=False)

    # Link to the lesson
    lesson_link = Column(String, nullable=False)

    # Add Date
    add_date = Column(DATE, default=datetime.date.today())


class ClassPresidents(BaseModel):
    __tablename__ = "class_presidents"

    # president id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)

    # president's group
    group_id = Column(Integer, nullable=False)

    # Add Date
    add_date = Column(DATE, default=datetime.date.today())
