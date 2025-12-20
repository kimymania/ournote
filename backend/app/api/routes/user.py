from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, Response

from app.api.dependencies import SessionDep, get_auth_user
from app.cache import get_id_by_username, remove_session
from app.constants import PWStringMetadata
from app.crud import authenticate_user, delete_db, get_user_rooms
from app.schemas import ReturnMessage, RoomsList, UserPrivate

router = APIRouter(tags=["user"])


@router.get(
    "/{username}",
    dependencies=[Depends(get_auth_user)],
    response_model=RoomsList,
    response_description="return list of rooms associated with user",
)
async def user_home(
    username: str,
    user_id: Annotated[UUID, Depends(get_id_by_username)],
    db: SessionDep,
):
    rooms = get_user_rooms(db, user_id)
    return rooms


@router.delete(
    "/{username}",
    response_model=ReturnMessage,
    response_description="ID of removed user",
)
async def delete_user(
    username: str,
    password: Annotated[str, Form(...), PWStringMetadata],
    user_id: Annotated[UUID, Depends(get_id_by_username)],
    session_id: Annotated[str, Depends(get_auth_user)],
    db: SessionDep,
    response: Response,
):
    creds = UserPrivate(username=username, id=user_id, password=password)
    data = authenticate_user(db, creds)
    result = delete_db(db, data)

    await remove_session(session_id)
    response.delete_cookie(key="Authorization")
    return result
