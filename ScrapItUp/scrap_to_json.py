from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
import json

from ScrapItUp.ids_dict import groups_ids
from bot.phrases import start_end_lessons, teachersFullNames, daysLongNames


PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


def lesson_1_or_togather(lesson) -> dict:

    lesson_name = lesson.find(
        string=True, recursive=False)[1:-1]  # Назвния уроков
    lesson_name = lesson_name.rsplit(' ', 2)
    teacher_short_name = lesson_name[1] + " " + lesson_name[2]
    teacher_full_name = teachersFullNames.get(teacher_short_name)
    lesson_name = lesson_name[0]

    lesson_cabinet = lesson.find('b')  # Все аудитории с урока

    discipline_id = int(lesson.get('title').split(', ')[1][9:-1])

    if lesson.find('i').text != "":  # Подгруппа чееек
        lesson_subgroup = lesson.find('i')  # Находим подгруппу если есть
        if '2' in lesson_subgroup.text:
            lesson_subgroup = 2
        elif '1' in lesson_subgroup.text:
            lesson_subgroup = 1
        else:
            lesson_subgroup = 0

    this_dict = {
        'LessonName': lesson_name,
        'TeacherShortName': teacher_short_name,
        'TeacherFullName': teacher_full_name,
        'LessonCabinet': lesson_cabinet.text[1:-3],
        'LessonType': lesson_cabinet.text[-2:],
        'DisciplineId': discipline_id,
        "LessonSubgroup": lesson_subgroup
    }
    return this_dict


def lesson_2subgroups(lesson) -> dict:

    lesson_names = lesson.find_all(string=True, recursive=False)

    first_lesson_name = lesson_names[0].text[1:-1].rsplit(' ', 2)
    first_teacher_short_name = first_lesson_name[1] + " " + first_lesson_name[2]
    first_teacher_long_name = teachersFullNames.get(first_teacher_short_name)

    second_lesson_name = lesson_names[1].text[1:-1].rsplit(' ', 2)
    second_teacher_short_name = second_lesson_name[1] + " " + second_lesson_name[2]
    second_teacher_long_name = teachersFullNames.get(second_teacher_short_name)

    lesson_cabinets = lesson.find_all('b')  # Все аудитории с урока

    discipline_id = int(lesson.get('title').split(', ')[1][9:-1])

    this_dict = {
        'LessonName': [first_lesson_name[0], second_lesson_name[0]],
        'TeacherShortName': [first_teacher_short_name, second_teacher_short_name],
        'TeacherFullName': [first_teacher_long_name, second_teacher_long_name],
        'LessonCabinet': [lesson_cabinets[0].text[1:-3], lesson_cabinets[1].text[1:-3]],
        'LessonType': [lesson_cabinets[0].text[-2:], lesson_cabinets[1].text[-2:]],
        'DisciplineId': discipline_id,
        'LessonSubgroup': -1
    }
    return this_dict


def week_scrap(this_week: list) -> dict:
    this_week_dict = {}
    week_info = this_week[0].text.split(" ")
    week_info = " ".join(week_info[:-1])
    this_week_dict["week_info"] = week_info + " тиждень"  # Неделя

    for i in range(1, 8):  # i - это день

        current_day_dict = {}
        k = 0

        day_date = this_week[i].find('td')  # ДАта 25.10
        current_day_dict['DayDate'] = day_date.text

        day_name_short = this_week[i].find_all('td')[1]  # Пн, Чт

        day_name_long = daysLongNames[day_name_short.text]
        current_day_dict['DayNameLong'] = day_name_long

        lessons = this_week[i].find_all('td')[2:]  # все уроки в ЭТОТ день

        for lesson in lessons:

            lesson_name = lesson.find_all(
                string=True, recursive=False)  # Назвния уроков
            if len(lesson_name) == 0:  # WTF
                continue  # А, точно! Там же пустые уроки бывают!

            if len(lesson_name) > 1:
                lesson_dict = lesson_2subgroups(lesson)
            else:
                lesson_dict = lesson_1_or_togather(lesson)
            # Номер урока; +1 тк начинаем с 0
            lesson_number = lessons.index(lesson)+1

            lesson_dict['LessonNumber'] = lesson_number
            lesson_dict['StartAt'] = start_end_lessons[lesson_number][0]
            lesson_dict['EndAt'] = start_end_lessons[lesson_number][1]

            current_day_dict[k] = lesson_dict
            k += 1

        this_week_dict[day_name_short.text] = current_day_dict

    return this_week_dict
# --------------------------------------------------------------------------------------


def scrap_html_to_json():
    for key, group_id in groups_ids.items():
        with open(f"{PATH}/ScrapItUp/Groups_html/{group_id}.html", "r", encoding="utf-8") as file:
            html = file.read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find_all('table')[1]
        trs = table.find_all('tr')
        # Все table rows таблицы

        # Первые два - лажа, дальше выбираем первые 8 (Рядок с неделей и 7 дней в неделе)
        # We need it in order to get next week already on weekends
        if (datetime.today().weekday() == 5) or (datetime.today().weekday() == 6):
            current_week = trs[10:18]
            next_week = trs[18:26]
        else:
            current_week = trs[2:10]
            next_week = trs[10:18]

        current_week_dict = week_scrap(current_week)
        next_week_dict = week_scrap(next_week)

        group_total_dict = {
            "current_week_dict": current_week_dict,
            "next_week_dict": next_week_dict
        }

        with open(f"{PATH}/ScrapItUp/Groups_json/{group_id}.json", "w") as outfile:
            json.dump(group_total_dict, outfile, indent=4, ensure_ascii=False)
