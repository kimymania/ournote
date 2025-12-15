from typing import Annotated

from fastapi import APIRouter, Depends, Form
from pydantic import Field

from app.api.dependencies import SessionDep, get_auth_user
from app.cache import generate_room_id
from app.core.security import hash_password
from app.crud import create_db
from app.models import Rooms
from app.schemas import Room, RoomCreate

router = APIRouter(tags=["room"])


@router.post(
    "/create_room",
    dependencies=[Depends(get_auth_user)],
    response_model=Room,
    response_description="ID of new room",
)
async def create_room(
    room_id: Annotated[str, Depends(generate_room_id)],
    password: Annotated[str, Form(...), Field(min_length=8, max_length=16)],
    db: SessionDep,
):
    room = RoomCreate(id=room_id, password=hash_password(password))
    data = Rooms(id=room.id, password=room.password)
    room = create_db(db, data)
    return room
