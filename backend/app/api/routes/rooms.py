from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form, HTTPException, status

from app.api.dependencies import SessionDep, get_auth_user
from app.cache import generate_room_id, get_id_by_username
from app.constants import RoomPINMetadata, UsernameStringMetadata
from app.core.security import hash_password
from app.crud import (
    add_user_to_room,
    authenticate_room,
    create_db,
    delete_db,
    get_room,
    get_user_rooms,
    user_leave_room,
)
from app.dbmodels import Rooms
from app.schemas import ReturnMessage, RoomPrivate, RoomPublic, RoomsList

router = APIRouter(tags=["room"])


@router.post(
    "/room",
    dependencies=[Depends(get_auth_user)],
    response_model=RoomPublic,
    response_description="ID of new room",
)
async def create_room(
    room_id: Annotated[str, Depends(generate_room_id)],
    password: Annotated[str, Form(...), RoomPINMetadata],
    username: Annotated[str, Body(...)],
    db: SessionDep,
):
    user_id = get_id_by_username(username)
    room_priv = RoomPrivate(id=room_id, password=hash_password(password))
    data = Rooms(id=room_priv.id, password=room_priv.password)
    room = create_db(db, data)

    add_user_to_room(db, user_id, room_id)
    return room


@router.get(
    "/room/{room_id}",
    dependencies=[Depends(get_auth_user)],
    response_model=RoomPublic,
    response_description="Room and list of items",
)
async def enter_room(
    room_id: str,
    db: SessionDep,
):
    room = RoomPublic(id=room_id)
    room = get_room(db, room.id)
    return room


@router.put(
    "/room/{room_id}",
    dependencies=[Depends(get_auth_user)],
    response_description="Joined room",
)
async def join_room(
    room_id: str,
    username: Annotated[str, Form(...), UsernameStringMetadata],
    password: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
):
    room = RoomPrivate(id=room_id, password=password)
    user_id = get_id_by_username(username)
    authenticate_room(db, room)

    result = add_user_to_room(db, user_id, room.id)
    if result["status"] != "successfully joined room":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already in room")
    msg = ReturnMessage(msg="successfully joined room")
    return msg


@router.delete(
    "/room/{room_id}",
    dependencies=[Depends(get_auth_user)],
    response_model=ReturnMessage,
    response_description="ID of removed room",
)
async def delete_room(
    room_id: str,
    password: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
):
    room = RoomPrivate(id=room_id, password=password)
    authenticate_room(db, room)

    data = Rooms(id=room.id, password=room.password)
    result = delete_db(db, data)
    return result


@router.delete(
    "/room/{room_id}/{username}",
    dependencies=[Depends(get_auth_user)],
    response_model=RoomsList,
    response_description="Updated list of user's rooms",
)
async def leave_room(
    room_id: str,
    username: str,
    password: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
):
    room = RoomPrivate(id=room_id, password=password)
    authenticate_room(db, room)

    user_id = get_id_by_username(username)
    result = user_leave_room(db, user_id, room.id)
    if result["status"] == "success":
        rooms_list = get_user_rooms(db, user_id)
        return rooms_list
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["status"])
