"""Pydantic schemas"""

from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GlobalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(GlobalBase):
    username: str


class UserCreate(User):
    id: UUID | None = None
    password: str


class UserPrivate(User):
    id: UUID
    password: str


class UserPublic(User):
    rooms: List[Room] | None = None


class Room(GlobalBase):
    id: str


class RoomPrivate(Room):
    password: str


class RoomPublic(Room):
    items: List[Item] = []


class RoomsList(GlobalBase):
    rooms: List[Room]


class Item(GlobalBase):
    title: str
