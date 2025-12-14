"""Server cache - might need external caching implementation"""

from functools import lru_cache
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import engine
from app.models import Users

# Replace with an actual cache database
SESSION_DB = {}


async def store_session(session_id: str, user_id: UUID) -> None:
    SESSION_DB[session_id] = user_id


async def remove_session(session_id: str) -> None:
    SESSION_DB.pop(session_id)


@lru_cache
def get_id_by_username(username: str) -> UUID:
    with Session(engine) as session:
        stmt = select(Users.id, Users.username).where(Users.username == username)
        result = session.execute(stmt).scalar_one()
        return result.id
