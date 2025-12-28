import random
import string
from typing import Annotated
from uuid import UUID

from fastapi import Form
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import SessionDep
from app.constants import RoomPINMetadata
from app.core.db import engine
from app.core.security import Authenticator
from app.crud import (
    add_user_to_room,
    create_db,
    delete_db,
    get_room_items,
    get_user_by_username,
    get_user_rooms,
    user_leave_room,
)
from app.dbmodels import Rooms
from app.exceptions import AuthenticationError, DBError
from app.schemas import BaseMessage, RoomPrivate, RoomPublic, RoomsList


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
) -> RoomPublic:
    """Create db entry -> add user to room"""
    room = RoomPrivate(id=room_id, password=auth.hash_password(room_pw))
    data = Rooms(**room.model_dump())
    try:
        create_db(db, data)
        add_user_to_room(db, user_id, room.id)
    except Exception as e:
        raise DBError(detail=f"{e}")

    room_pub = RoomPublic(id=room.id)
    return room_pub


async def enter_room(
    room_id: str,
    room_pw: str,
    db: SessionDep,
    auth: Authenticator,
) -> RoomPublic:
    room = auth.authenticate_room(db, room_id, room_pw)
    result = get_room_items(db, room.id)
    return result


async def join_room(
    user_id: UUID,
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: Authenticator,
) -> BaseMessage:
    room = auth.authenticate_room(db, room_id, room_pw)
    try:
        result = add_user_to_room(db, user_id, room.id)
    except Exception as e:
        raise DBError(detail=f"{e}")
    return BaseMessage(message=result["message"])


async def delete_room(
    room_id: str,
    room_pw: str,
    db: SessionDep,
    auth: Authenticator,
) -> dict[str, str]:
    room = auth.authenticate_room(db, room_id, room_pw)
    result = delete_db(db, room.id)
    return result


async def leave_room(
    user_id: UUID,
    username: str,
    password: str,
    room_id: str,
    db: SessionDep,
    auth: Authenticator,
) -> RoomsList:
    user = get_user_by_username(db, username)
    if not auth.verify_password(password, user.password):
        raise AuthenticationError("Wrong password")

    user_leave_room(db, user_id, room_id)
    rooms_list = get_user_rooms(db, user_id)
    return rooms_list
