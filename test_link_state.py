import os
import tempfile


with tempfile.TemporaryDirectory() as directory:
    os.environ["DATABASE_PATH"] = os.path.join(directory, "comverify.db")
    from database import initialize_database, is_server_linked
    from server import link_dashboard_server

    initialize_database()
    assert not is_server_linked("123456789")
    link_dashboard_server(
        project_id=42,
        project_name="Contract Test Project",
        owner_id="987654321",
        guild_id="123456789",
        guild_name="Contract Test Guild",
    )
    assert is_server_linked("123456789")
    print("ComVerify local login state OK")
