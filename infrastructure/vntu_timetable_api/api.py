import logging
from typing import Any

from infrastructure.vntu_timetable_api.base import BaseClient


class VntuTimetableApi(BaseClient):
    def __init__(self):
        self.base_url = "https://vm4625529.25ssd.had.wf"
        super().__init__(base_url=self.base_url)

    async def get_faculties(self) -> tuple[int, dict[str, Any]]:
        try:
            status, faculties = await self._make_request(method="get", url="/v0/faculties")
            await self.close()
            return status, faculties
        except Exception as e:
            logging.error(e)
            await self.close()
            return 0, {}

    async def get_group_timetable(self, group_id: int):
        try:
            status, group_timetable = await self._make_request(method="get", url=f"/v0/groups/{group_id}")
            await self.close()
            return status, group_timetable
        except Exception as e:
            logging.error(e)
            await self.close()
            return 0, {}
