from typing import Any, Type
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from app.dbmodels import Items, Rooms, Users
from app.dbmodels import room_membership as RoomMem
from app.exceptions import DBError, NotFoundError
from app.schemas import (
    Item,
    ItemsList,
    Result,
    Room,
    RoomPrivate,
    RoomsList,
    UserPrivate,
)


def create_db(db: Session, data: object) -> Result:
    record = data.__repr__()  # so i don't have to add a refresh() after commit()
    try:
        db.add(data)
        db.commit()
    except IntegrityError:
        db.rollback()
        return Result(success=False, detail=f"{record} already exists in DB", status_code=409)
    except SQLAlchemyError:
        db.rollback()
        return Result(success=False, detail="DB error", status_code=500)
    return Result(detail="succesfully created")


TABLE_ID_REGISTRY: dict[Any, Type] = {
    UUID: Users,
    str: Rooms,
    int: Items,
}


def delete_db(db: Session, id: Any, **kwargs) -> Result:
    """:params data: any of User ID, Room ID or Item ID"""
    table = TABLE_ID_REGISTRY.get(type(id))
    if table is None:
        raise DBError("Unknown type")

    stmt = delete(table).where(table.id == id)
    if isinstance(table, Items):
        room_id = kwargs["room_id"]
        stmt = stmt.where(table.room_id == room_id)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return Result(success=False, detail=f"error: {e}")
    return Result(detail="successfully deleted")


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


def user_leave_room(db: Session, user_id: UUID, room_id: str) -> Result:
    """Remove user from room membership"""
    stmt = delete(RoomMem).where(RoomMem.c.user_id == user_id).where(RoomMem.c.room_id == room_id)
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        # raise DBError from e
        return Result(success=False, detail="failed to leave room", data=e)
    return Result(detail="leave room successful")


def insert_if_not_exists(db: Session, data: dict[str, Any]) -> Result:
    if not db.bind:  # Suppress db.bind.dialect linter error - should not happen
        raise DBError("Session is corrupt")

    if db.bind.dialect.name == "postgresql":
        insert = pg_insert
    else:
        insert = sqlite_insert
    stmt = insert(RoomMem).values(**data)
    pkeys = [c.name for c in RoomMem.primary_key]
    try:
        db.execute(stmt.on_conflict_do_nothing(index_elements=pkeys))
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return Result(success=False, detail="DB operation failure", data=e, status_code=500)
    return Result(detail="successfully entered room")


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


def get_all_room_items(db: Session, room_id: str) -> ItemsList:
    """:returns: list of all items in room"""
    stmt = select(Items.id, Items.title).where(Items.room_id == room_id)
    result = db.execute(stmt).all()
    if len(result) == 0:
        return ItemsList()
    items = [Item(id=item[0], title=item[1]) for item in result]
    items_list = ItemsList(items=items)
    return items_list


def get_item(db: Session, data: Items) -> Result:
    stmt = select(Items).where(Items.room_id == data.room_id).where(Items.id == data.id)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        return Result(success=False, detail="item doesn't exist")
    item = Item(id=result.id, title=result.title, content=result.content)
    return Result(detail="item found", data=item)


def update_item(db: Session, data: Items) -> Result:
    item = Item(id=data.id, title=data.title, content=data.content)
    stmt = (
        update(Items)
        .where(Items.room_id == data.room_id)
        .where(Items.id == data.id)
        .values(title=data.title, content=data.content)
    )
    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    result = Result(detail="successfully updated item", data=item)
    return result
