def timetable_message_generator(
    timetable: dict, group_name: str, subgroup: int
) -> dict[str, list[str]]:
    match subgroup:
        case 1:
            subgroup_text = ", 1 підгрупа"
        case 2:
            subgroup_text = ", 2 підгрупа"
        case _:
            subgroup_text = ""
    group_header = f"{group_name}" + subgroup_text

    first_week_list = []
    second_week_list = []
    for week, days in timetable["data"].items():
        for day in days:
            date_header = (
                f"{day['date']} ({day['day']},"
                + ("1-ий тиждень" if week == "firstWeek" else "2-ий тиждень")
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
                second_week_list.append("\n".join([group_header, date_header, *lessons]))

    return {
        "firstWeek": first_week_list,
        "secondWeek": second_week_list,
    }


def convert_lesson(lesson: dict) -> str:
    return f""" 
num: {lesson["num"]}
auditory: {lesson["auditory"]}
type: {lesson["type"]}
name: {lesson["name"]}
begin: {lesson["begin"]}
end: {lesson["end"]}
teacher: {lesson["teacher"]["name"]}\n
    """
