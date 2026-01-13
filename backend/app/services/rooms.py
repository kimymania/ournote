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
    edit_room_data,
    get_all_room_items,
    get_user_by_username,
    insert_if_not_exists,
    user_leave_room,
)
from app.dbmodels import Rooms
from app.exceptions import AuthenticationError
from app.schemas import ItemsList, Result, RoomCreate


def generate_room_id() -> Result:
    """Generate unique 8-character ID string for rooms

    Resulting ID is in Result.data"""
    while True:
        result: str = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        with Session(engine) as session:
            match = session.execute(select(Rooms.id).where(Rooms.id == result)).scalar_one_or_none()
            if match is None:
                return Result(detail="successfully created unique id", data=result)


async def create_room(
    user_id: UUID,
    room_id: str,
    room_name: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    """Create room and add user - room membership"""
    room = RoomCreate(id=room_id, name=room_name, password=auth.hash_password(room_pw))
    data = Rooms(**room.model_dump())
    create_result = create_db(db, data)
    if not create_result.success:
        return create_result
    membership = {"user_id": user_id, "room_id": room.id}
    insert_result = insert_if_not_exists(db, membership)
    return insert_result


async def join_room(
    user_id: UUID,
    room_id: str,
    room_pw: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    """Once user enters a room, user stays a member unless they 'leave' the room"""
    room = auth.auth_room(db, room_id, room_pw)
    data = {"user_id": user_id, "room_id": room.id}
    result = insert_if_not_exists(db, data)
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
    room = auth.auth_room(db, room_id, room_pw)
    result = delete_db(db, room.id)
    return result


async def leave_room(
    user_id: UUID,
    username: str,
    password: str,
    room_id: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    user = get_user_by_username(db, username)
    if user.id != user_id or not auth.verify_password(password, user.password):
        raise AuthenticationError()
    result = user_leave_room(db, user_id, room_id)
    return result


async def edit_room_details(
    room_id: str,
    room_name: str,
    db: Session,
) -> Result:
    result = edit_room_data(
        db=db,
        room_id=room_id,
        room_name=room_name,
    )
    return result
