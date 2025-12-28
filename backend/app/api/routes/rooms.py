from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form

from app.api.dependencies import AuthDep, SessionDep
from app.constants import PWStringMetadata, RoomPINMetadata
from app.core.security import get_current_user
from app.schemas import BaseMessage, RoomPublic, RoomsList
from app.services import rooms as service

router = APIRouter(prefix="/room", tags=["room"])


@router.post("/{room_id}", response_model=RoomPublic, response_description="ID of created room")
async def create_room(
    user_id: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    return await service.create_room(
        user_id=user_id,
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )


@router.get(
    "/{room_id}",
    response_model=RoomPublic,
    response_description="Room and list of items",
)
async def enter_room(
    _: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    """Enter joined room

    WIP - get method should only return values -> use POST to check password"""
    return await service.enter_room(
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )


@router.put("/{room_id}")
async def join_room(
    user_id: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    return await service.join_room(
        user_id=user_id,
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )


@router.delete("/{room_id}", response_model=BaseMessage)
async def delete_room(
    _: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    return await service.delete_room(
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )


@router.delete(
    "/{room_id}/{username}",
    response_model=RoomsList,
    response_description="Updated list of rooms",
)
async def leave_room(
    user_id: Annotated[UUID, Depends(get_current_user)],
    username: str,
    password: Annotated[str, Form(...), PWStringMetadata],
    room_id: str,
    db: SessionDep,
    auth: AuthDep,
):
    return await service.leave_room(
        user_id=user_id,
        username=username,
        password=password,
        room_id=room_id,
        db=db,
        auth=auth,
    )
