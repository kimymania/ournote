from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form
from starlette import status
from starlette.responses import Response

from app.api.dependencies import AuthDep, SessionDep
from app.constants import PWStringMetadata, RoomIDMetadata, RoomPINMetadata
from app.core.security import get_current_user
from app.exceptions import DBError, DuplicateDataError
from app.schemas import ItemsList
from app.services import rooms as service

router = APIRouter(prefix="/room", tags=["room"])


@router.post("/create", status_code=201)
async def create_room(
    user_id: Annotated[UUID, Depends(get_current_user)],
    room_id: Annotated[str, Form(...), RoomIDMetadata],
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    result = await service.create_room(
        user_id=user_id,
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )
    if result.success:
        return
    if result.status_code == 409:
        raise DuplicateDataError
    elif result.status_code == 500:
        raise DBError


@router.post("/{room_id}", response_class=Response)
async def join_room(
    user_id: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    result = await service.join_room(
        user_id=user_id,
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )
    if result.success:
        return Response(status_code=status.HTTP_200_OK)
    if result.status_code == 500:
        raise DBError


@router.get("/{room_id}", response_model=ItemsList, response_description="list of items in room")
async def get_room_contents(
    _: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    db: SessionDep,
):
    result = await service.get_room_contents(room_id=room_id, db=db)
    return result


@router.delete("/{room_id}", response_class=Response)
async def delete_room(
    _: Annotated[UUID, Depends(get_current_user)],
    room_id: str,
    room_pw: Annotated[str, Form(...), RoomPINMetadata],
    db: SessionDep,
    auth: AuthDep,
):
    result = await service.delete_room(
        room_id=room_id,
        room_pw=room_pw,
        db=db,
        auth=auth,
    )
    if result.success:
        return Response(status_code=status.HTTP_200_OK)
    raise DBError


@router.delete(
    "/{room_id}/{username}",
    response_class=Response,
)
async def leave_room(
    user_id: Annotated[UUID, Depends(get_current_user)],
    username: str,
    password: Annotated[str, Form(...), PWStringMetadata],
    room_id: str,
    db: SessionDep,
    auth: AuthDep,
):
    result = await service.leave_room(
        user_id=user_id,
        username=username,
        password=password,
        room_id=room_id,
        db=db,
        auth=auth,
    )
    if result.success:
        return Response(status_code=status.HTTP_200_OK)
    raise DBError
