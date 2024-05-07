import logging
from typing import Any

from aiohttp import ClientError

from infrastructure.vntu_timetable_api.base import BaseClient


class VntuTimetableApi(BaseClient):
    """Class for making requests to VNTU Timetable API."""

    def __init__(self):
        self.base_url = "https://vm4625529.25ssd.had.wf"
        super().__init__(base_url=self.base_url)

    async def get_faculties(self) -> tuple[int, dict[str, Any]]:
        """Method to get faculties data."""
        try:
            return await self.make_request(method="get", url="/v0/faculties")
        except ClientError as ce:
            logging.error("Error getting faculties: %s", ce)
            return 0, {}

    async def get_group_timetable(self, group_id: int) -> tuple[int, dict[str, Any]]:
        """Method to get group timetable data."""
        try:
            return await self.make_request(method="get", url=f"/v0/groups/{group_id}")
        except ClientError as ce:
            logging.error(
                "Error getting group timetable: %s | Group id: %i", ce, group_id
            )
            return 0, {}
