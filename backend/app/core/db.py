from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

POSTGRESQL_URI = ""
engine = create_engine(POSTGRESQL_URI, echo=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
