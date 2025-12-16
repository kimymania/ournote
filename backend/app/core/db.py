from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLITE_URI = "sqlite:///local.db"
engine = create_engine(SQLITE_URI, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db(**kwargs):
    if "engine" in kwargs.keys():
        Base.metadata.create_all(bind=kwargs["engine"])
    Base.metadata.create_all(bind=engine)
