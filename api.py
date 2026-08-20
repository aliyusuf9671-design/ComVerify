import os

import aiohttp


COMVERIFY_API_URL = os.getenv(
    "COMVERIFY_API_URL",
    "http://localhost:3000"
)

COMVERIFY_API_KEY = os.getenv(
    "COMVERIFY_API_KEY"
)


class ComVerifyAPI:
    def __init__(self):
        self.base_url = COMVERIFY_API_URL.rstrip("/")
        self.api_key = COMVERIFY_API_KEY

    async def request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None
    ):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["Authorization"] = (
                f"Bearer {self.api_key}"
            )

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                json=data,
                headers=headers
            ) as response:

                try:
                    result = await response.json()
                except Exception:
                    result = {
                        "success": False,
                        "error": await response.text()
                    }

                return response.status, result

    async def login_server(
        self,
        project_key: str,
        guild_id: str,
        guild_name: str,
        owner_id: str
    ):
        return await self.request(
            "POST",
            "/api/servers/login",
            {
                "project_key": project_key,
                "guild_id": guild_id,
                "guild_name": guild_name,
                "owner_id": owner_id
            }
        )

    async def get_project(
        self,
        guild_id: str
    ):
        return await self.request(
            "GET",
            f"/api/servers/{guild_id}"
        )


api = ComVerifyAPI()
