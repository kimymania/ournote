"""Server cache - might need external caching implementation"""

import random
import string
from functools import lru_cache
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import engine
from app.models import Rooms, Users

# Replace with an actual cache database
SESSION_DB = {}


async def store_session(session_id: str, user_id: UUID) -> None:
    SESSION_DB[session_id] = user_id


async def remove_session(session_id: str) -> None:
    SESSION_DB.pop(session_id)


@lru_cache
def get_id_by_username(username: str) -> UUID:
    with Session(engine) as session:
        stmt = select(Users.id).where(Users.username == username)
        user_id = session.execute(stmt).scalar_one()
        return user_id


@lru_cache
def generate_room_id() -> str:
    while True:
        result = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        with Session(engine) as session:
            match = session.execute(select(Rooms.id).where(Rooms.id == result)).scalar_one_or_none()
            if match is None:
                return result
