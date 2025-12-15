from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies import SessionDep, get_auth_user
from app.cache import get_id_by_username
from app.crud import get_user_rooms
from app.schemas import RoomsList

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
