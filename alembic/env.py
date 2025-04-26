import sys
import os
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context

# Explicitly add 'src/' to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

# Alembic Config
config = context.config

# Logging setup
if config.config_file_name:
    fileConfig(config.config_file_name)

# Database URL (from Render env)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Import Base and models for Alembic
from core.database import Base  # ✅ Database Base

# ✅ Import all models at once (avoids duplication)
from models import *  # This loads everything via __init__.py

target_metadata = Base.metadata  # ✅ This connects all models

# Run migrations online
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()