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


class UserLogin(User):
    password: str


class UserPrivate(User):
    id: UUID
    password: str


class Room(GlobalBase):
    id: str


class RoomCreate(Room):
    password: str


class RoomsList(GlobalBase):
    rooms: List[Room]


class Item(GlobalBase):
    title: str
