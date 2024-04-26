from infrastructure.vntu_timetable_api.base import BaseClient


class VntuTimetableApi(BaseClient):
    def __init__(self):
        self.base_url = "https://vm4625529.25ssd.had.wf"
        super().__init__(base_url=self.base_url)

    async def get_faculties(self):
        return await self._make_request(method="get", url="/v0/faculties")
