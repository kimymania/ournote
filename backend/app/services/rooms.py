import random
import string
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import engine
from app.core.security import Authenticator
from app.crud import (
    create_db,
    delete_db,
    get_all_room_items,
    get_user_by_username,
    upsert_room_membership,
    user_leave_room,
)
from app.dbmodels import Rooms
from app.exceptions import AuthenticationError
from app.schemas import ItemsList, Result, RoomPrivate, RoomsList


def generate_room_id() -> Result:
    """Generate unique 8-character ID string for rooms

    Resulting ID is in Result.data"""
    while True:
        result = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        with Session(engine) as session:
            match = session.execute(select(Rooms.id).where(Rooms.id == result)).scalar_one_or_none()
            if match is None:
                return Result(detail="successfully created unique id", data=result)


async def create_room(
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    """Only create room - client will handle room enter immediately after creation"""
    room = RoomPrivate(id=room_id, password=auth.hash_password(room_pw))
    data = Rooms(**room.model_dump())
    result = create_db(db, data)
    return result


async def enter_room(
    user_id: UUID,
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    """Once user enters a room, user stays a member unless they 'leave' the room"""
    room = auth.authenticate_room(db, room_id, room_pw)
    result = upsert_room_membership(db, user_id, room.id)
    return result


async def get_room_contents(
    room_id: str,
    db: Session,
) -> ItemsList:
    """Authentication and authorization should be completed beforehand.
    After that, client uses this function to get all the room items"""
    result = get_all_room_items(db, room_id)
    return result


async def delete_room(
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    room = auth.authenticate_room(db, room_id, room_pw)
    result = delete_db(db, room.id)
    return result


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
