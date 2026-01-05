"""Pydantic schemas"""

from typing import Any, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GlobalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Token(GlobalBase):
    access_token: str
    token_type: str = "bearer"


class Result(GlobalBase):
    success: bool = True
    detail: str
    data: Any | None = None
    status_code: int | None = None


class User(GlobalBase):
    username: str
    password: str

    model_config = ConfigDict(str_strip_whitespace=True)


class UserCreate(User):
    id: UUID | None = None


class UserPrivate(User):
    id: UUID


class RoomsList(GlobalBase):
    rooms: List[Room] | None = None


class Room(GlobalBase):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: str


class RoomPrivate(Room):
    password: str


class ItemsList(GlobalBase):
    items: List[Item] | None = None


class Item(GlobalBase):
    id: int | None = None
    title: str
    content: str | None = None


class ItemModifier(Item):
    room_id: str


class ItemPrivate(GlobalBase):
    item_id: int
    room_id: str
