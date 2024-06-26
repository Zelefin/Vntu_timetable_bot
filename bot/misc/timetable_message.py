lesson_types = {"ЛК": "ЛК🟨", "ПЗ": "ПЗ🟩", "ЛР": "ЛР🟦"}

lesson_number = {
    1: "1⃣",
    2: "2⃣",
    3: "3⃣",
    4: "4⃣",
    5: "5⃣",
    6: "6⃣",
    7: "7⃣",
    8: "8⃣",
    9: "9⃣",
    10: "🔟",
    11: "1⃣1⃣",
    12: "1⃣2⃣",
    13: "1⃣3⃣",
    14: "1⃣4⃣",
}

days_long_names = {
    "Пн": "Понеділок",
    "Вт": "Вівторок",
    "Ср": "Середа",
    "Чт": "Четвер",
    "Пт": "П'ятниця",
    "Сб": "Субота",
    "Нд": "Неділя",
}


def timetable_message_generator(
    timetable: dict, group_name: str, subgroup: int
) -> dict[str, list[str]]:
    """
    Converts timetable dictionary (as a response form API) to prettified dictionary.

    :argument timetable: timetable dictionary (as a response form API).
    :argument group_name: group name.
    :argument subgroup: subgroup (0 or 1 or 2).
    :returns Prettified dictionary with 1-st and 2-nd weeks. Only for specific subgroup.
    """
    match subgroup:
        case 1:
            subgroup_text = ", 1 Підгрупа"
        case 2:
            subgroup_text = ", 2 Підгрупа"
        case _:
            subgroup_text = ""
    group_header = f"┌ 👥{group_name}" + subgroup_text

    first_week_list = []
    second_week_list = []
    for week, days in timetable["data"].items():
        for day in days:
            date_header = (
                f"└ 🗓<b>{day['date']}</b> ({days_long_names[day['day']]}, "
                + ("1-ий Тиждень" if week == "firstWeek" else "2-ий Тиждень")
                + ")\n"
            )
            lessons = []
            for lesson in day["lessons"]:
                if lesson["subgroup"] != 0 and lesson["subgroup"] != subgroup:
                    continue
                lessons.append(convert_lesson(lesson))
            if len(lessons) == 0:
                lessons.append("<b>Уроків немає🏖</b>")

            if week == "firstWeek":
                first_week_list.append("\n".join([group_header, date_header, *lessons]))
            else:
                second_week_list.append(
                    "\n".join([group_header, date_header, *lessons])
                )

    return {
        "firstWeek": first_week_list,
        "secondWeek": second_week_list,
    }


def convert_lesson(lesson: dict) -> str:
    """Converts lesson from dict to prettified string"""
    lesson_header = (
        f"{lesson_number[lesson['num']]} ⎪ <i>"
        f"<b>{lesson['begin']} - {lesson['end']}</b></i> ⎪ "
        + (
            lesson_types.get(lesson["type"])
            if lesson_types.get(lesson["type"])
            else str(lesson["type"]) + "🟥"
        )
        + "\n"
    )
    lesson_body = (
        f"<b>┗ {lesson['name']}</b>\n"
        f"💼 {lesson['teacher']['name']}\n"
        f"🏫 {lesson['auditory']}\n"
    )
    return lesson_header + lesson_body
