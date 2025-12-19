"""Server cache - might need external caching implementation"""

import random
import string
from functools import lru_cache
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db import engine
from app.dbmodels import Rooms, Users

# Replace with an actual cache database
SESSION_DB = {}


async def store_session(session_id: str, user_id: UUID) -> None:
    SESSION_DB[session_id] = user_id


async def remove_session(session_id: str) -> None:
    SESSION_DB.pop(session_id)


async def get_user_id(session_id: str) -> UUID:
    return SESSION_DB[session_id]


@lru_cache
def get_id_by_username(username: str) -> UUID:
    """Get user ID for internal use

    Raises a 500 error if User ID isn't found, but this shouldn't actually happen"""
    username = username.strip()
    with Session(engine) as session:
        stmt = select(Users.id).where(Users.username == username)
        try:
            user_id = session.execute(stmt).scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"can't find id of {username}",
            )
        return user_id


@lru_cache
def generate_room_id() -> str:
    while True:
        result = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        with Session(engine) as session:
            match = session.execute(select(Rooms.id).where(Rooms.id == result)).scalar_one_or_none()
            if match is None:
                return result
