from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os

# Allow override via environment variable for tests or runtime configuration.
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    BASE_DIR = os.path.dirname(__file__)
    DB_PATH = os.path.join(BASE_DIR, "app.db")
    DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with check_same_thread only for sqlite file-based or memory
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
# If using in-memory sqlite, use StaticPool so the same connection (and schema) is reused
if DATABASE_URL == "sqlite:///:memory:" or DATABASE_URL.startswith("sqlite:///:memory:"):
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    # Import models here to register with Base
    from models_db import User, Token
    Base.metadata.create_all(bind=engine)
