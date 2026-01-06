from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form

from app.api.dependencies import AuthDep, SessionDep
from app.constants import PWStringMetadata, UsernameStringMetadata
from app.core.security import get_current_user
from app.exceptions import DBError, DuplicateDataError
from app.schemas import RoomsList
from app.services import user as service

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup", status_code=201)
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
    if result.success:
        return
    raise DuplicateDataError


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


@router.delete("/{username}", status_code=200)
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
    if result.success:
        return
    raise DBError
