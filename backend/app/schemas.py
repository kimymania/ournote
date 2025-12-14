"""Pydantic schemas"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    id: UUID | None = None
    password: str
    model_config = ConfigDict(from_attributes=True)
