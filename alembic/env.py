import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from logging.config import fileConfig
from alembic import context
import os

# Read Alembic config
config = context.config

# Setup logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Read DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Target metadata (import your models)
from core.database import Base
target_metadata = Base.metadata

# Run migrations
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
