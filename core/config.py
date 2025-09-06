# File: core/config.py
"""
Central Tortoise ORM config.
Uses project_config/dealcross_config.py for DB URL.
Relies on models/__init__.py exports for discovery.
"""

from project_config.dealcross_config import settings

DATABASE_URL = settings.get_effective_database_url()

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "models",          # auto-discover all exported models
                "aerich.models",   # aerich metadata
            ],
            "default_connection": "default",
        }
    },
}
