"""Pydantic schemas"""

from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GlobalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Token(GlobalBase):
    access_token: str
    token_type: str = "bearer"


class BaseMessage(GlobalBase):
    success: bool = True
    message: str


class Generator(GlobalBase):
    generated_id: str


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
    title: str
    content: str | None = None


class ItemCreate(Item):
    id: int | None = None
    title: str
    content: str | None = None
    room_id: str
