from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, text
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from app.core.security import verify_password
from app.dbmodels import Items, Rooms, Users, room_membership
from app.schemas import (
    ItemPublic,
    ReturnMessage,
    RoomBase,
    RoomPrivate,
    RoomPublic,
    RoomsList,
    UserPrivate,
    UserPublic,
)


def get_username_match(db: Session, username: str) -> bool:
    stmt = select(Users).where(Users.username == username)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        return False
    return True


T = TypeVar("T")


def create_db(db: Session, data: object) -> UserPublic | RoomPublic | ItemPublic:
    """:params data: any of Users, Rooms or Items"""
    if isinstance(data, Users):
        r = UserPublic(username=data.username)
    elif isinstance(data, Rooms):
        r = RoomPublic(id=data.id)
    elif isinstance(data, Items):
        r = ItemPublic(title=data.title, content=data.content)
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


def delete_db(db: Session, data: object) -> ReturnMessage:
    """:params data: any of Users, Rooms or Items

    Associated data should be removed automatically - NEEDS FIXING"""
    if isinstance(data, Users):
        table = Users
        r = data.username
    elif isinstance(data, Rooms):
        table = Rooms
        r = data.id
    elif isinstance(data, Items):
        table = Items
        r = data.title
    else:
        raise
    msg = ReturnMessage(msg=f"{r} deleted")

    try:
        stmt = delete(table).where(table.id == data.id)
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return msg


def add_user_to_room(db: Session, user_id: UUID, room_id: str) -> dict[str, str]:
    # Need to check if user has already joined the room
    try:
        db.execute(insert(room_membership).values(user_id=user_id, room_id=room_id))
        db.commit()
    except IntegrityError:
        return {"status": "user is already in room"}
    return {"status": "successfully joined room"}


def authenticate_user(db: Session, data: UserPrivate) -> UserPrivate:
    stmt = select(Users).where(Users.id == data.id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result or not verify_password(data.password, result.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = UserPrivate(id=result.id, username=result.username, password=result.password)
    return user


def authenticate_room(db: Session, data: RoomPrivate) -> None:
    stmt = select(Rooms).where(Rooms.id == data.id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room doesn't exist")
    if not verify_password(data.password, result.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong passcode")
    return


def get_user_rooms(db: Session, user_id: UUID) -> RoomsList:
    stmt = select(room_membership).where(room_membership.c.user_id == user_id)
    result = db.execute(stmt).all()
    if result is None:
        rooms_list = RoomsList(rooms=[])
    else:
        rooms_list = RoomsList(rooms=[RoomBase(id=r.room_id) for r in result])
    return rooms_list


# def get_user_rooms(db: Session, user_id: UUID) -> RoomsList:
#     result = db.execute(
#         text("""
#             SELECT rooms.id FROM rooms
#             WHERE users.id = :user_id_var
#             """),
#         {"user_id_var": user_id}
#     ).one_or_none()


def get_room(db: Session, room_id: str) -> RoomPublic:
    """:returns: Room ID & List of items in room"""
    result = db.execute(
        text("""
            SELECT rooms.id, items.title FROM rooms
            LEFT JOIN items ON items.room_id = rooms.id
            WHERE rooms.id = :room_id_var
            """),
        {"room_id_var": room_id},
    ).all()
    if len(result) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room doesn't exist")

    id = result[0].id
    items = [ItemPublic(title=item_title) for _, item_title in result if item_title]
    room = RoomPublic(id=id, items=items)
    return room


def get_item_data(db: Session, data: Items) -> ItemPublic:
    stmt = select(Items).where(Items.room_id == data.room_id).where(Items.id == data.id)
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item doesn't exist")
    item = ItemPublic(title=result.title, content=result.content)
    return item


def update_item(db: Session, data: Items) -> ItemPublic:
    stmt = (
        update(Items)
        .where(Items.room_id == data.room_id)
        .where(Items.id == data.id)
        .values(title=data.title, content=data.content)
    )
    item = ItemPublic(title=data.title, content=data.content)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return item
