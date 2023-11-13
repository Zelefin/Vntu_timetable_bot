from pathlib import Path
import json

from sqlalchemy.ext.asyncio import async_sessionmaker
from ScrapItUp.ids_dict import groups_ids
from bot.db.db_functions import add_lesson, drop_lessons_table
from bot.phrases import days_short

PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


async def main_parsing_to_db(session_maker: async_sessionmaker):
    await drop_lessons_table(session_maker=session_maker)
    for _, group_id in groups_ids.items():
        with open(f'{PATH}/ScrapItUp/Groups_json/{group_id}.json', 'r') as json_file:
            json_data = json.load(json_file)

        current_week: dict = json_data['current_week_dict']

        for day_short in days_short:
            date = current_week[day_short]["DayDate"]
            for key, day in current_week.items():
                if isinstance(day, dict) and key == day_short:
                    for key2, lesson in day.items():
                        if isinstance(lesson, dict):
                            if lesson['LessonSubgroup'] == -1:
                                await add_lesson(session_maker=session_maker,
                                                 group_id=int(group_id),
                                                 subgroup=1,
                                                 lesson_name=lesson['LessonName'][0],
                                                 lesson_type=lesson['LessonType'][0],
                                                 teacher_short_name=lesson['TeacherShortName'][0],
                                                 lesson_time_start=lesson['StartAt'],
                                                 lesson_date_start=date)
                                await add_lesson(session_maker=session_maker,
                                                 group_id=int(group_id),
                                                 subgroup=2,
                                                 lesson_name=lesson['LessonName'][1],
                                                 lesson_type=lesson['LessonType'][1],
                                                 teacher_short_name=lesson['TeacherShortName'][1],
                                                 lesson_time_start=lesson['StartAt'],
                                                 lesson_date_start=date)
                            else:
                                await add_lesson(session_maker=session_maker,
                                                 group_id=int(group_id),
                                                 subgroup=int(lesson['LessonSubgroup']),
                                                 lesson_name=lesson['LessonName'],
                                                 lesson_type=lesson['LessonType'],
                                                 teacher_short_name=lesson['TeacherShortName'],
                                                 lesson_time_start=lesson['StartAt'],
                                                 lesson_date_start=date)
