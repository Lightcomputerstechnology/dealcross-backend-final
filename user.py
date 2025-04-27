from sqlalchemy import Table, MetaData
from core.database import engine

# ✅ Reflect the existing 'users' table from the database
metadata = MetaData()
User = Table('users', metadata, autoload_with=engine)
