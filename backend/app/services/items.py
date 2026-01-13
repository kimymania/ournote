from typing import Any

from sqlalchemy.orm import Session

from app.crud import create_db, delete_db, get_item, update_item
from app.dbmodels import Items
from app.schemas import Item, ItemModifier, ItemPrivate, Result


async def create_item(
    room_id: str,
    db: Session,
    title: str,
    content_json: list[Any],
) -> Result:
    create = ItemModifier(title=title, content_json=content_json, room_id=room_id)
    data = Items(**create.model_dump())
    result = create_db(db, data)
    return result


async def view_existing_item(
    room_id: str,
    item_id: int,
    db: Session,
) -> Item | None:
    priv = ItemPrivate(item_id=item_id, room_id=room_id)
    data = Items(id=priv.item_id, room_id=priv.room_id)
    result = get_item(db, data)
    item = result.data
    return item


async def edit_item(
    room_id: str,
    item_id: int,
    db: Session,
    title: str,
    content_json: list[Any],
) -> Item | None:
    edit = ItemModifier(id=item_id, title=title, content_json=content_json, room_id=room_id)
    data = Items(**edit.model_dump())
    result = update_item(db, data)
    item = result.data
    return item


async def delete_item(
    room_id: str,
    item_id: int,
    db: Session,
) -> Result:
    priv = ItemPrivate(room_id=room_id, item_id=item_id)
    result = delete_db(db, id=priv.item_id, room_id=priv.room_id)
    return result
