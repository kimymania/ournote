from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form

from app.api.dependencies import AuthDep, SessionDep
from app.constants import PWStringMetadata, UsernameStringMetadata
from app.core.security import get_current_user
from app.schemas import BaseMessage, RoomsList
from app.services import user as service

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup", response_model=BaseMessage)
async def create_user(
    username: Annotated[str, Form(...), UsernameStringMetadata],
    password: Annotated[str, Form(...), PWStringMetadata],
    auth: AuthDep,
    db: SessionDep,
):
    result = await service.create_user(
        username=username,
        password=password,
        db=db,
        auth=auth,
    )
    return result


@router.get("/{username}", response_model=RoomsList, response_description="list of user's rooms")
async def user_home(
    username: str,
    user_id: Annotated[UUID, Depends(get_current_user)],
    db: SessionDep,
):
    rooms = await service.get_user_home(
        user_id=user_id,
        username=username,
        db=db,
    )
    return rooms


@router.delete("/{username}", response_model=BaseMessage)
async def delete_user(
    user_id: Annotated[UUID, Depends(get_current_user)],
    password: Annotated[str, Form(...)],
    auth: AuthDep,
    db: SessionDep,
):
    result = await service.delete_user(
        user_id=user_id,
        auth=auth,
        password=password,
        db=db,
    )
    return result
