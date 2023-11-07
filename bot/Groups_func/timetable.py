from bot.days_weeks_stuff import cur_week
from pathlib import Path

from ScrapItUp.ids_dict import groups_ids


PATH = Path.cwd()

if PATH.name == "bot":
    PATH = PATH.parent


def send_lessons(user_info, day: int, week=cur_week()) -> str:

    group = str(user_info['group'])  # group id
    subgroup = str(user_info['subgroup'])  # its integer already

    with open(str(PATH) + "/ScrapItUp/Groups/" + group + "/" +
              str(week) + "/" + str(day) + "/IP" + subgroup + ".txt", "r", encoding="utf8") as text:

        return text.read()
