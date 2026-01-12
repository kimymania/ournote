"""SQLAlchemy database models"""

import uuid
from typing import Any, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

room_membership = Table(
    "room_membership",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("room_id", ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True),
)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=lambda: uuid.uuid4())
    username: Mapped[str] = mapped_column(String(16), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    rooms: Mapped[List[Rooms]] = relationship(secondary=room_membership, back_populates="members")


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    name: Mapped[str] = mapped_column(String(16), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    members: Mapped[list[Users]] = relationship(secondary=room_membership, back_populates="rooms")
    items: Mapped[list[Items]] = relationship(back_populates="room", cascade="all, delete-orphan")


class Items(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    content: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    content_json: Mapped[list[Any]] = mapped_column(JSONB)
    room_id: Mapped[str] = mapped_column(
        String(8),
        ForeignKey("rooms.id", ondelete="CASCADE"),
        primary_key=False,
    )

    room: Mapped[Rooms] = relationship(back_populates="items")
