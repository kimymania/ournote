"""Pydantic schemas"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str


class UserCreate(User):
    id: UUID | None = None
    password: str
