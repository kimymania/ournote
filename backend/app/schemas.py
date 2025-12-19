"""Pydantic schemas"""

from typing import Annotated, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints

USERNAME_PATTERN = r"^[a-zA-Z0-9-_\.]+$"

UsernameRule = Annotated[
    str,
    StringConstraints(
        min_length=2,
        max_length=16,
        pattern=USERNAME_PATTERN,
        strict=True,
    ),
]


class GlobalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReturnMessage(GlobalBase):
    msg: str


class UserBase(GlobalBase):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: UsernameRule


class UserCreate(UserBase):
    id: UUID | None = None
    password: str


class UserPrivate(UserBase):
    id: UUID
    password: str


class UserPublic(UserBase):
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
