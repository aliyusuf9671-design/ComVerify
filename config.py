import json
import os
from pathlib import Path


CONFIG_DIRECTORY = Path(
    os.getenv("CONFIG_DIRECTORY", "config")
)

CONFIG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


def get_config_path(guild_id: str) -> Path:
    return CONFIG_DIRECTORY / f"{guild_id}.json"


def default_config() -> dict:
    return {
        "verification": {
            "enabled": True,
            "channel_id": None,
            "title": "Verify with ComVerify",
            "description": (
                "Click the button below to begin "
                "verification."
            ),
            "color": 0x5865F2,
            "button_text": "Verify",
            "button_emoji": "✅",
            "verification_url": None
        },

        "backup": {
            "enabled": True,
            "retention_days": 30
        },

        "recovery": {
            "enabled": True
        }
    }


def load_config(guild_id: str) -> dict:
    path = get_config_path(guild_id)

    if not path.exists():
        config = default_config()
        save_config(guild_id, config)
        return config

    try:
        with path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        config = default_config()
        save_config(guild_id, config)
        return config


def save_config(
    guild_id: str,
    config: dict
) -> None:
    path = get_config_path(guild_id)

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            config,
            file,
            indent=4
        )


def update_config(
    guild_id: str,
    section: str,
    setting: str,
    value
) -> dict:

    config = load_config(guild_id)

    if section not in config:
        config[section] = {}

    config[section][setting] = value

    save_config(
        guild_id,
        config
    )

    return config
