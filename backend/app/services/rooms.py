import random
import string
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import engine
from app.core.security import Authenticator
from app.crud import (
    add_user_to_room,
    create_db,
    delete_db,
    get_room_items,
    get_user_by_username,
    upsert_room_membership,
    user_leave_room,
)
from app.dbmodels import Rooms
from app.exceptions import AuthenticationError
from app.schemas import ItemsList, RoomPrivate, RoomsList


def generate_room_id() -> str:
    """Generate unique 8-character ID string for rooms"""
    while True:
        result = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        with Session(engine) as session:
            match = session.execute(select(Rooms.id).where(Rooms.id == result)).scalar_one_or_none()
            if match is None:
                return result


async def create_room(
    user_id: UUID,
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> str:
    """Create db entry -> add user to room"""
    room = RoomPrivate(id=room_id, password=auth.hash_password(room_pw))
    data = Rooms(**room.model_dump())
    create_db(db, data)
    add_user_to_room(db, user_id, room.id)
    return "room created"


async def enter_room(
    user_id: UUID,
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> str:
    room = auth.authenticate_room(db, room_id, room_pw)
    upsert_room_membership(db, user_id, room.id)
    return "room entered"


async def get_room_contents(
    room_id: str,
    db: Session,
) -> ItemsList:
    result = get_room_items(db, room_id)
    return result


async def delete_room(
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> str:
    room = auth.authenticate_room(db, room_id, room_pw)
    delete_db(db, room.id)
    return "delete successful"


async def leave_room(
    user_id: UUID,
    username: str,
    password: str,
    room_id: str,
    db: Session,
    auth: Authenticator,
) -> RoomsList:
    user = get_user_by_username(db, username)
    if user.id != user_id or not auth.verify_password(password, user.password):
        raise AuthenticationError()
    rooms = user_leave_room(db, user_id, room_id)
    return rooms
