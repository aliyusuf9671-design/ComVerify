import os

import aiohttp


COMVERIFY_API_URL = os.getenv(
    "COMVERIFY_API_URL",
    "https://comverifydas-yjyffaj4.manus.space"
)


class ComVerifyAPI:
    """Small async client for the ComVerify dashboard bot contract."""

    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or COMVERIFY_API_URL).rstrip("/")

    async def request(self, method: str, endpoint: str, data: dict | None = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.request(method, url, json=data, headers=headers) as response:
                try:
                    result = await response.json()
                except Exception:
                    result = {"success": False, "error": await response.text()}
                return response.status, result

    async def login_server(self, project_key: str, guild_id: str, guild_name: str, owner_id: str):
        return await self.request("POST", "/api/login", {"project_key": project_key.strip(), "guild_id": str(guild_id), "guild_name": guild_name, "owner_id": str(owner_id)})

    async def create_backup(self, project_key: str, guild_id: str, snapshot: dict):
        return await self.request("POST", "/api/bot/backups", {"project_key": project_key, "guild_id": str(guild_id), "snapshot": snapshot})

    async def list_backups(self, project_key: str, guild_id: str):
        return await self.request("GET", f"/api/bot/backups?project_key={project_key}&guild_id={guild_id}")

    async def fetch_backup(self, project_key: str, guild_id: str, backup_id: int):
        return await self.request("POST", "/api/bot/backups/restore", {"project_key": project_key, "guild_id": str(guild_id), "backup_id": backup_id})

    async def complete_restore(self, project_key: str, guild_id: str, backup_id: int):
        return await self.request("POST", "/api/bot/backups/restore/complete", {"project_key": project_key, "guild_id": str(guild_id), "backup_id": backup_id})

    async def fail_restore(self, project_key: str, guild_id: str, backup_id: int, error: str):
        return await self.request("POST", "/api/bot/backups/restore/failed", {"project_key": project_key, "guild_id": str(guild_id), "backup_id": backup_id, "error": error})

    async def get_settings(self, project_key: str, guild_id: str):
        return await self.request("GET", f"/api/bot/settings?project_key={project_key}&guild_id={guild_id}")

    async def update_settings(self, project_key: str, guild_id: str, settings: dict):
        return await self.request("PUT", "/api/bot/settings", {"project_key": project_key, "guild_id": str(guild_id), **settings})


api = ComVerifyAPI()
