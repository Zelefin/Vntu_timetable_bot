from bot.days_weeks_stuff import cur_week
from ScrapItUp.ids_dict import groups_ids
from pathlib import Path

PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


async def send_lessons(user_info: dict, day: int, week: int) -> str:
    # We can't set values by default, because they're changing
    group = str(user_info['group'])  # group id
    subgroup = str(user_info['subgroup'])  # its integer already

    # TODO: bro...
    group_name = next((key for key, value in groups_ids.items() if value == group), None)

    if subgroup != "0":
        header = f"┌ {group_name}, {subgroup} Підгрупа\n"
    else:
        header = f"┌ {group_name}\n"
        subgroup = "1"

    try:
        with open(str(PATH) + "/ScrapItUp/Groups/" + group + "/" +
                  str(week) + "/" + str(day) + "/IP" + subgroup + ".txt", "r", encoding="utf8") as text:

            return header + text.read()

    except FileNotFoundError:
        return "Отакої! Файла не знайдено!😳\nНапишіть будь ласка про це у <i>/feedback</i>"
