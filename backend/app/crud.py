from typing import Any, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, text
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from app.dbmodels import Items, Rooms, Users
from app.dbmodels import room_membership as RoomMem
from app.exceptions import DBError, DuplicateDataError, NotFoundError
from app.schemas import (
    Item,
    ItemsList,
    Room,
    RoomPrivate,
    RoomsList,
    UserPrivate,
)


def create_db(db: Session, data: object) -> None:
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
    except IntegrityError as e:
        db.rollback()
        raise DuplicateDataError(data.__repr__()) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise DBError from e


TABLE_ID_REGISTRY: dict[Any, Type] = {
    UUID: Users,
    str: Rooms,
    int: Items,
}


def delete_db(db: Session, id: Any) -> None:
    """:params data: any of User ID, Room ID or Item ID"""
    table = TABLE_ID_REGISTRY.get(type(id))
    if table is None:
        raise DBError("Unknown type")

    stmt = delete(table).where(table.id == id)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DBError from e


def get_user_by_username(db: Session, username: str) -> UserPrivate:
    stmt = select(Users).where(Users.username == username)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise NotFoundError(f"user of {username} doesn't exist")
    user = UserPrivate(id=result.id, username=result.username, password=result.password)
    return user


def get_user_by_id(db: Session, user_id: UUID) -> UserPrivate:
    stmt = select(Users).where(Users.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        raise NotFoundError(detail="user doesn't exist")
    user = UserPrivate(id=result.id, username=result.username, password=result.password)
    return user


def add_user_to_room(db: Session, user_id: UUID, room_id: str) -> None:
    stmt = insert(RoomMem).values(user_id=user_id, room_id=room_id)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def user_leave_room(db: Session, user_id: UUID, room_id: str) -> RoomsList:
    """Remove user from room membership -> Return updated rooms list"""
    stmt1 = delete(RoomMem).where(RoomMem.c.user_id == user_id).where(RoomMem.c.room_id == room_id)
    stmt2 = select(RoomMem).where(RoomMem.c.user_id == user_id)
    try:
        db.execute(stmt1)
        result = db.execute(stmt2).all()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    rooms_list = RoomsList(rooms=[Room(id=r.room_id) for r in result] if result else None)
    return rooms_list


def upsert_room_membership(db: Session, user_id: UUID, room_id: str) -> None:
    """Check if user is a member of room -> If not, create record"""
    try:
        db.execute(
            text("""
                INSERT INTO room_membership (user_id, room_id)
                VALUES (:user_id, :room_id)
                ON CONFLICT (user_id, room_id) DO NOTHING
                """),
            {"user_id": user_id, "room_id": room_id},
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def get_user_rooms(db: Session, user_id: UUID) -> RoomsList:
    stmt = select(RoomMem).where(RoomMem.c.user_id == user_id)
    result = db.execute(stmt).all()
    rooms_list = RoomsList(rooms=[Room(id=r.room_id) for r in result] if result else None)
    return rooms_list


def get_room(db: Session, room_id: str) -> RoomPrivate:
    stmt = select(Rooms.id, Rooms.password).where(Rooms.id == room_id)
    result = db.execute(stmt).one_or_none()
    if not result:
        raise NotFoundError(detail="room doesn't exist")
    id, password = result.tuple()
    room = RoomPrivate(id=id, password=password)
    return room


def get_room_items(db: Session, room_id: str) -> ItemsList:
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

    items = [Item(title=item_title) for _, item_title in result if item_title]
    items_list = ItemsList(items=items)
    return items_list


def get_item_data(db: Session, data: Items) -> Item:
    stmt = select(Items).where(Items.room_id == data.room_id).where(Items.id == data.id)
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise NotFoundError(detail="item doesn't exist")
    item = Item(title=result.title, content=result.content)
    return item


def update_item(db: Session, data: Items) -> Item:
    stmt = (
        update(Items)
        .where(Items.room_id == data.room_id)
        .where(Items.id == data.id)
        .values(title=data.title, content=data.content)
    )
    item = Item(title=data.title, content=data.content)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    return item
