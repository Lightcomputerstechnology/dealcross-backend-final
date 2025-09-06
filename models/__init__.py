# File: models/__init__.py
"""
Auto-import all model submodules in this package so Tortoise can see them,
without hardcoding each filename.

Benefits:
- No crashes if a file is renamed (e.g., auditlog.py → audit_log.py).
- New model files are picked up automatically.
- Keeps Aerich/Tortoise discovery stable with "models" in TORTOISE_ORM.
"""

import pkgutil
import importlib
from pathlib import Path

_pkg_path = Path(__file__).parent

# Import every *.py module (except private/dunder) under models/
for _mod in pkgutil.iter_modules([str(_pkg_path)]):
    name = _mod.name
    if name.startswith("_") or name == "__init__":
        continue
    importlib.import_module(f"{__name__}.{name}")

# Tortoise doesn’t need __all__, but keep namespace clean explicitly.
__all__ = []