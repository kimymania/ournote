from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models import Rooms, Users, room_membership
from app.schemas import Item, Room, RoomsList, User, UserLogin, UserPrivate


def get_username_match(db: Session, username: str) -> bool:
    stmt = select(Users).where(Users.username == username)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        return False
    return True


T = TypeVar("T")


def create_db(db: Session, data: T) -> User | Room | Item:
    """:params data: any of Users, Rooms or Items"""
    if isinstance(data, Users):
        r = User(username=data.username)
    elif isinstance(data, Rooms):
        r = Room(id=data.id)
    elif isinstance(data, Item):
        r = Item(title=data.title)
    else:
        raise

    try:
        db.add(data)
        db.commit()
        db.refresh(data)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return r


# def create_user(db: Session, data: Users) -> User:
#     try:
#         user = User(username=data.username)
#         db.add(data)
#         db.commit()
#         db.refresh(data)
#         return user
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise e


# def create_room(db: Session, data: Rooms) -> Room:
#     try:
#         room = Room(id=data.id)
#         db.add(data)
#         db.commit()
#         db.refresh(data)
#         return room
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise e


def authenticate_user(db: Session, data: UserLogin) -> UserPrivate:
    stmt = select(Users).where(Users.username == data.username)
    result = db.execute(stmt).scalar_one_or_none()
    if not result or not verify_password(data.password, result.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = UserPrivate(id=result.id, username=result.username, password=result.password)
    return user


def get_user_rooms(db: Session, user_id: UUID) -> RoomsList:
    stmt = (
        select(Rooms.id)
        .join(room_membership, Users.id == room_membership.c.user_id)
        .join(room_membership, Rooms.id == room_membership.c.room_id)
        .where(Users.id == user_id)
    )
    result = db.execute(stmt).scalars()
    rooms_list = RoomsList(rooms=[Room(id=r) for r in result])
    return rooms_list
