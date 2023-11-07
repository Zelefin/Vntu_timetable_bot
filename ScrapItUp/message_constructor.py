import json
from pathlib import Path


PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


groups_ids = {
    "1ПІ-23б": "10679",
    "2ПІ-23б": "10680",
    "3ПІ-23б": "10681",
    "4ПІ-23б": "10682",
    "5ПІ-23б": "10839",
    "6ПІ-23б": "10840"
}

nameDaysShort = ["Пн", "Вт", "Ср", "Чт", "Пт"]

lessonTypes = {
    "ЛК": "ЛК🟨",
    "ПЗ": "ПЗ🟩",
    "ЛР": "ЛР🟦"
}


def add_lesson(lesson: dict) -> str:
    lesson_number = "Номер уроку: " + str(lesson['LessonNumber'])
    lesson_start_end = "⏰З <b>" + \
        lesson['StartAt'] + "</b> До <b>" + lesson['EndAt'] + "</b>"
    lesson_name_type = "Назва: <b>" + \
        lesson['LessonName'] + ", " + \
        lessonTypes[f"{lesson['LessonType']}"] + "</b>"

    if lesson.get('TeacherFullName') is not None:
        lesson_teacher_name = "Викладач: " + lesson['TeacherFullName']
    else:
        lesson_teacher_name = "Викладач: " + lesson['TeacherShortName']

    lesson_cabinet = "Аудиторія: <b>" + lesson['LessonCabinet'] + "</b>"

    return f"""{lesson_number}
{lesson_start_end}
{lesson_name_type}
{lesson_teacher_name}
{lesson_cabinet}\n
"""


def divide_sub_lesson(lesson: dict):
    first_sub_lesson = {
        "LessonName": lesson['LessonName'][0],
        "TeacherShortName": lesson['TeacherShortName'][0],
        "TeacherFullName": lesson['TeacherFullName'][0],
        "LessonCabinet": lesson['LessonCabinet'][0],
        "LessonType": lesson['LessonType'][0],
        "LessonNumber": lesson['LessonNumber'],
        "StartAt": lesson['StartAt'],
        "EndAt": lesson['EndAt']
    }
    second_sub_lesson = {
        "LessonName": lesson['LessonName'][1],
        "TeacherShortName": lesson['TeacherShortName'][1],
        "TeacherFullName": lesson['TeacherFullName'][1],
        "LessonCabinet": lesson['LessonCabinet'][1],
        "LessonType": lesson['LessonType'][1],
        "LessonNumber": lesson['LessonNumber'],
        "StartAt": lesson['StartAt'],
        "EndAt": lesson['EndAt']
    }
    divided_lessons = [add_lesson(first_sub_lesson), add_lesson(second_sub_lesson)]
    return divided_lessons


def constructor(current_week: dict):

    total_week_1_subgroup = []
    total_week_2_subgroup = []

    for dayShort in nameDaysShort:

        current_day_lessons = []
        str_current_day_1sub = ""
        str_current_day_2sub = ""

        for key, day in current_week.items():
            if isinstance(day, dict) and key == dayShort:
                date = f"> 🗓{day['DayDate']} ({day['DayNameLong']})\n\n"
                str_current_day_1sub += date
                str_current_day_2sub += date
                for key2, lesson in day.items():
                    if isinstance(lesson, dict):
                        current_day_lessons.append(lesson)

        for lesson in current_day_lessons:

            if lesson['LessonSubgroup'] == -1:
                string_lesson = divide_sub_lesson(lesson)
                str_current_day_1sub += string_lesson[0]
                str_current_day_2sub += string_lesson[1]

            elif lesson['LessonSubgroup'] == 0:
                string_lesson = add_lesson(lesson)
                str_current_day_1sub += string_lesson
                str_current_day_2sub += string_lesson

            elif lesson['LessonSubgroup'] == 1:
                string_lesson = add_lesson(lesson)
                str_current_day_1sub += string_lesson

            elif lesson['LessonSubgroup'] == 2:
                string_lesson = add_lesson(lesson)
                str_current_day_2sub += string_lesson

        total_week_1_subgroup.append(str_current_day_1sub[:-2])
        total_week_2_subgroup.append(str_current_day_2sub[:-2])

    return [total_week_1_subgroup, total_week_2_subgroup]


def week_construct(week: str) -> None:
    for key, group_id in groups_ids.items():
        with open(f'{PATH}/ScrapItUp/Groups_json/{group_id}.json', 'r') as json_file:
            json_data = json.load(json_file)

        group_num = key[:-6]

        current_week = constructor(json_data[week])

        week_num = json_data[week]['week_info'][0]

        i = 1
        for day in current_week[0]:
            with open(f'{PATH}/ScrapItUp/Groups/{week_num}/{group_num}/{i}/IP1.txt', 'w') as f:
                f.write(f"> {key}, 1 Підгрупа\n" + day)
            i += 1

        i = 1
        for day in current_week[1]:
            with open(f'{PATH}/ScrapItUp/Groups/{week_num}/{group_num}/{i}/IP2.txt', 'w') as f:
                f.write(f"> {key}, 2 Підгрупа\n" + day)
            i += 1

# ------------------------------------------------------------------------


def weeks_constructor():
    week_construct('current_week_dict')
    week_construct('next_week_dict')
