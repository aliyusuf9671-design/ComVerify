import asyncio

from api import ComVerifyAPI


async def main():
    client = ComVerifyAPI("https://comverifydas-yjyffaj4.manus.space")
    status, payload = await client.login_server(
        project_key="CV-INVALID-TEST-KEY",
        guild_id="123456789",
        guild_name="Contract Test",
        owner_id="987654321",
    )
    assert status == 401, (status, payload)
    assert payload.get("success") is False
    assert "key" in payload.get("error", "").lower()
    print("ComVerify bot contract OK: /api/login returned expected 401 for invalid key")


if __name__ == "__main__":
    asyncio.run(main())
