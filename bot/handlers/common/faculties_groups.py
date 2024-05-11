import json
from typing import Any

from redis.asyncio import Redis

from infrastructure.vntu_timetable_api import VntuTimetableApi


async def get_faculties(redis: Redis, api: VntuTimetableApi) -> dict[str, Any]:
    """
    Function to get faculties.
    :param redis: redis instance
    :param api: api instance
    :return: faculties dict
    """
    if faculties_redis := await redis.get("faculties"):
        faculties = json.loads(faculties_redis)
    else:
        response, faculties = await api.get_faculties()
        if response != 200 or not faculties:
            return {}
        await redis.set("faculties", json.dumps(faculties), ex=1800)
    return faculties


def find_group(faculties: dict[str, Any], group_name: str) -> tuple[Any, Any, Any]:
    """
    Find group by its name in faculties dict.
    :param faculties: faculties dict (as response from API)
    :param group_name: name of the group to find
    :return: faculty id, group id, group name (normalized)
    """
    for faculty in faculties.get("data"):
        for group in faculty["groups"]:
            if group["name"].upper() == group_name.upper():
                return faculty["id"], group["id"], group["name"]
    return None, None, None
