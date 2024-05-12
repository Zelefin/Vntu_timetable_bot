import json

from redis.asyncio import Redis

from bot.misc.timetable_message import timetable_message_generator
from infrastructure.database.models import User
from infrastructure.vntu_timetable_api import VntuTimetableApi


async def get_timetable(
    user: User, redis: Redis, api: VntuTimetableApi, week: str, day: int
) -> str | None:
    if timetable_list := await redis.get(str(user.group_id) + str(user.subgroup)):
        timetable = json.loads(timetable_list)[week][day]
    else:
        status, timetable_response = await api.get_group_timetable(
            group_id=user.group_id
        )
        if status != 200 or not timetable_response:
            return
        timetable_list = timetable_message_generator(
            timetable=timetable_response,
            group_name=user.group_name,
            subgroup=user.subgroup,
        )
        await redis.set(
            str(user.group_id) + str(user.subgroup), json.dumps(timetable_list), ex=1800
        )
        timetable = timetable_list[week][day]

    return timetable
