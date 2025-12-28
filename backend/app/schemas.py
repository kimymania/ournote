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


class UserPublic(GlobalBase):
    username: str
    rooms: List[RoomPublic] = []


class RoomBase(GlobalBase):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: str


class RoomPrivate(RoomBase):
    password: str


class RoomPublic(RoomBase):
    items: List[ItemPublic] = []


class RoomsList(GlobalBase):
    rooms: List[RoomBase]


class ItemBase(GlobalBase):
    pass


class ItemCreate(ItemBase):
    id: int | None = None
    title: str
    content: str = ""
    room_id: str


class ItemPrivate(ItemBase):
    id: int
    room_id: str


class ItemPublic(ItemBase):
    title: str
    content: str = ""
