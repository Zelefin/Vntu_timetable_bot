from bot.days_weeks_stuff import cur_week
from pathlib import Path


PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


async def send_lessons(user_info, day: int, week=cur_week()) -> str:

    group = str(user_info['group'])  # group id
    subgroup = str(user_info['subgroup'])  # its integer already

    try:
        with open(str(PATH) + "/ScrapItUp/Groups/" + group + "/" +
                  str(week) + "/" + str(day) + "/IP" + subgroup + ".txt", "r", encoding="utf8") as text:

            return text.read()
    except FileNotFoundError:
        return "Отакої! Файла не знайдено!😳\nНапишіть будь ласка про це у <i>/feedback</i>"
