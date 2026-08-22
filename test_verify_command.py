import asyncio
from unittest.mock import patch

from verification import send_verification_embed


class FakeResponse:
    def __init__(self):
        self.deferred = False
        self.messages = []

    async def defer(self, **kwargs):
        self.deferred = True

    async def send_message(self, *args, **kwargs):
        self.messages.append((args, kwargs))


class FakeFollowup:
    def __init__(self):
        self.messages = []

    async def send(self, *args, **kwargs):
        self.messages.append((args, kwargs))


class FakeGuild:
    id = 123456789


class FakeInteraction:
    guild = FakeGuild()

    def __init__(self):
        self.response = FakeResponse()
        self.followup = FakeFollowup()


class FakeAPI:
    async def get_settings(self, project_key, guild_id):
        return 200, {"success": True, "settings": {"embedTitle": "Verify here"}}


def test_verify_defers_before_dashboard_request_and_sends_panel():
    interaction = FakeInteraction()
    with patch("verification.get_login_context", return_value={"project_key": "CV-12345678", "dashboard_server_id": 987}), patch("verification.ComVerifyAPI", return_value=FakeAPI()):
        asyncio.run(send_verification_embed(interaction))
    assert interaction.response.deferred is True
    assert len(interaction.followup.messages) == 1
    assert interaction.followup.messages[0][1]["view"] is not None


def test_verify_reports_missing_login_after_acknowledgement():
    interaction = FakeInteraction()
    with patch("verification.get_login_context", return_value=None):
        asyncio.run(send_verification_embed(interaction))
    assert interaction.response.deferred is True
    assert "isn't set up" in interaction.followup.messages[0][0][0]
