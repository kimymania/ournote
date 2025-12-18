"""Pydantic schemas"""

from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GlobalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReturnMessage(GlobalBase):
    msg: str


class UserBase(GlobalBase):
    username: str


class UserCreate(UserBase):
    id: UUID | None = None
    password: str


class UserPrivate(UserBase):
    id: UUID
    password: str


class UserPublic(UserBase):
    rooms: List[RoomPublic] = []


class RoomBase(GlobalBase):
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
