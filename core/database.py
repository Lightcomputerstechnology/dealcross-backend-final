from __future__ import annotations

import os
import logging
import subprocess
from tortoise import Tortoise

from project_config.dealcross_config import settings

logger = logging.getLogger("dealcross.db")

# Effective DB URL (handles postgresql:// → postgres://)
DATABASE_URL = settings.get_effective_database_url()

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                # Keep the broad auto-discovery plus aerich’s own model
                "models",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}

AUTO_SCHEMA = os.getenv("AUTO_SCHEMA", "0")  # default OFF to avoid cyclic-FK error
ALLOW_AERICH_SUBPROCESS = os.getenv("ALLOW_AERICH_SUBPROCESS", "1")  # allow fallback by default


def _run(cmd: str) -> None:
    """Run a shell command and log stdout/stderr."""
    logger.info("▶ %s", cmd)
    proc = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if proc.stdout:
        logger.info(proc.stdout.strip())
    if proc.stderr:
        logger.warning(proc.stderr.strip())
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd} (exit={proc.returncode})")


def _ensure_aerich_ini_present() -> None:
    """Ensure there is an aerich.ini at repo root."""
    if not os.path.isfile("aerich.ini"):
        raise RuntimeError("aerich.ini not found at repo root")


def _bootstrap_with_aerich():
    """
    Programmatic Aerich bootstrap:
    - If migrations folder already exists, run `aerich upgrade`.
    - Else do `aerich init -t core.config.TORTOISE_ORM` then `aerich init-db`.
    """
    _ensure_aerich_ini_present()

    has_migrations = os.path.isdir("migrations") and os.path.isfile("migrations/models/__init__.py")

    if has_migrations:
        # Try upgrade path
        try:
            _run("aerich upgrade")
            return
        except Exception:
            logger.warning("aerich upgrade failed, attempting init-db fallback…")

    # Fresh init (first boot)
    _run("aerich init -t core.config.TORTOISE_ORM || true")
    _run("aerich init-db")


async def init_db():
    """
    Initialize Tortoise. Strategy:

    1) Try a clean init.
    2) If AUTO_SCHEMA=1, attempt generate_schemas(safe=True).
       - If it raises cyclic-FK error, and ALLOW_AERICH_SUBPROCESS=1,
         bootstrap schema via Aerich CLI, then re-init.
    3) Otherwise, leave schema untouched (assumes Aerich ran previously).
    """
    # First init
    logger.info("🔌 Initializing Tortoise ORM…")
    await Tortoise.init(config=TORTOISE_ORM)

    # Auto schema path (optional)
    if AUTO_SCHEMA in ("1", "true", "True", "yes", "on"):
        try:
            logger.info("🛠️ AUTO_SCHEMA enabled → generating schemas (safe=True)…")
            await Tortoise.generate_schemas(safe=True)
            logger.info("✅ Schemas verified/created.")
            return
        except Exception as e:
            msg = str(e)
            logger.error("❌ generate_schemas failed: %s", msg)

            # If this is the cyclic-FK case, try Aerich fallback (subprocess)
            if "cyclic fk references" in msg.lower() and ALLOW_AERICH_SUBPROCESS in ("1", "true", "True", "yes", "on"):
                logger.warning("♻️ Detected cyclic-FK. Falling back to Aerich bootstrap…")
                try:
                    _bootstrap_with_aerich()
                    # Re-init Tortoise to pick up created schema
                    await Tortoise.close_connections()
                    await Tortoise.init(config=TORTOISE_ORM)
                    logger.info("✅ Tortoise re-initialized after Aerich bootstrap.")
                    return
                except Exception as e2:
                    logger.error("❌ Aerich bootstrap failed: %s", e2)
                    raise
            # Not cyclic or fallback disabled → bubble up
            raise
    else:
        logger.info("ℹ️ AUTO_SCHEMA disabled; assuming schema is managed by Aerich.")

    logger.info("✅ Tortoise ORM initialized successfully.")


async def close_db():
    """Close all Tortoise ORM connections gracefully."""
    try:
        await Tortoise.close_connections()
        logger.info("✅ Tortoise connections closed successfully.")
    except Exception as e:
        logger.error("❌ Failed to close Tortoise connections: %s", e)