from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form
from pydantic import Field

from app.api.dependencies import SessionDep
from app.cache import generate_room_id, get_id_by_username
from app.core.security import hash_password
from app.crud import add_user_to_room, authenticate_room, create_db, delete_db, get_room
from app.dbmodels import Rooms
from app.schemas import Room, RoomPrivate, RoomPublic

router = APIRouter(tags=["room"])


@router.post(
    "/room",
    # dependencies=[Depends(get_auth_user)],
    response_model=Room,
    response_description="ID of new room",
)
async def create_room(
    room_id: Annotated[str, Depends(generate_room_id)],
    password: Annotated[str, Form(...), Field(min_length=4, max_length=4)],
    username: Annotated[str, Body(...)],
    db: SessionDep,
):
    room = RoomPrivate(id=room_id, password=hash_password(password))
    data = Rooms(id=room.id, password=room.password)
    room = create_db(db, data)

    user_id = get_id_by_username(username)
    add_user_to_room(db, user_id, room_id)
    return room


@router.get(
    "/room/{room_id}",
    # dependencies=[Depends(get_auth_user)],
    response_model=RoomPublic,
    response_description="Room and list of items",
)
async def enter_room(
    room_id: str,
    db: SessionDep,
):
    room = Room(id=room_id)
    room = get_room(db, room.id)
    return room


@router.put(
    "/room/{room_id}",
    # dependencies=[Depends(get_auth_user)],
    response_description="Joined room",
)
async def join_room(
    room_id: str,
    password: Annotated[str, Form(...), Field(min_length=4, max_length=4)],
    username: Annotated[str, Body(...)],
    db: SessionDep,
):
    room = RoomPrivate(id=room_id, password=password)
    user_id = get_id_by_username(username)
    authenticate_room(db, room)

    result = add_user_to_room(db, user_id, room.id)
    return result


@router.delete(
    "/room/{room_id}",
    # dependencies=[Depends(get_auth_user)],
    response_model=Room,
    response_description="Removed room",
)
async def delete_room(
    room_id: str,
    password: Annotated[str, Form(...), Field(min_length=4, max_length=4)],
    db: SessionDep,
):
    room = RoomPrivate(id=room_id, password=password)
    authenticate_room(db, room)

    data = Rooms(id=room.id, password=room.password)
    result = delete_db(db, data)
    return result
