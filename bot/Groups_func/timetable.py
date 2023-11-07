from bot.days_weeks_stuff import cur_week
from pathlib import Path
PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


def send_lessons(user_info, day: int, week=cur_week()) -> str:

    group = user_info['group'][0]
    subgroup = user_info['subgroup'][0]

    with open(str(PATH) + "/ScrapItUp/Groups/" + str(week) + "/" +
              group + "/" + str(day) + "/IP" + subgroup + ".txt", "r", encoding="utf8") as text:

        return text.read()
