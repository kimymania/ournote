from typing import Any, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, text
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from app.dbmodels import Items, Rooms, Users, room_membership
from app.exceptions import DBError, NotFoundError
from app.schemas import (
    ItemPublic,
    RoomBase,
    RoomPrivate,
    RoomPublic,
    RoomsList,
    UserPrivate,
)


def create_db(db: Session, data: object) -> dict[str, str]:
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return {"message": "success"}


TABLE_ID_REGISTRY: dict[Any, Type] = {
    UUID: Users,
    str: Rooms,
    int: Items,
}


def delete_db(db: Session, id: Any) -> dict[str, str]:
    """:params data: any of User ID, Room ID or Item ID"""
    table = TABLE_ID_REGISTRY.get(type(id))
    if not table:
        raise DBError

    stmt = delete(table).where(table.id == id)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return {"message": "success"}


def get_user_by_username(db: Session, username: str) -> UserPrivate:
    stmt = select(Users).where(Users.username == username)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise NotFoundError
    user = UserPrivate(id=result.id, username=result.username, password=result.password)
    return user


def get_user_by_id(db: Session, user_id: UUID) -> UserPrivate:
    stmt = select(Users).where(Users.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise NotFoundError(detail="user doesn't exist")
    user = UserPrivate(id=result.id, username=result.username, password=result.password)
    return user


def add_user_to_room(db: Session, user_id: UUID, room_id: str) -> dict[str, str]:
    stmt = insert(room_membership).values(user_id=user_id, room_id=room_id)
    try:
        db.execute(stmt)
        db.commit()
    except IntegrityError as e:
        raise e
    except SQLAlchemyError as e:
        raise e
    return {"message": "success"}


def user_leave_room(db: Session, user_id: UUID, room_id: str) -> dict[str, str]:
    stmt = (
        delete(room_membership)
        .where(room_membership.c.user_id == user_id)
        .where(room_membership.c.room_id == room_id)
    )
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return {"message": "success"}


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


def get_room(db: Session, room_id: str) -> RoomPrivate:
    stmt = select(Rooms.id, Rooms.password).where(Rooms.id == room_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise NotFoundError(detail="room doesn't exist")
    id, password = result
    room = RoomPrivate(id=id, password=password)
    return room


def get_room_items(db: Session, room_id: str) -> RoomPublic:
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
        raise NotFoundError(detail="room doesn't exist")

    items = [ItemPublic(title=item_title) for _, item_title in result if item_title]
    room = RoomPublic(id=room_id, items=items)
    return room


def get_item_data(db: Session, data: Items) -> ItemPublic:
    stmt = select(Items).where(Items.room_id == data.room_id).where(Items.id == data.id)
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise NotFoundError(detail="item doesn't exist")
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
