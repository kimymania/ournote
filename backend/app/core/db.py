from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=settings.dev)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db(**kwargs):
    Base.metadata.drop_all(bind=engine)
    if "engine" in kwargs.keys():
        Base.metadata.create_all(bind=kwargs["engine"])
    Base.metadata.create_all(bind=engine)


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Sets SQLite constraints ON"""
    if isinstance(dbapi_connection, SQLite3Connection):
        # the sqlite3 driver will not set PRAGMA foreign_keys
        # if autocommit=False; set to True temporarily
        ac = dbapi_connection.autocommit
        dbapi_connection.autocommit = True

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

        # restore previous autocommit setting
        dbapi_connection.autocommit = ac
