from typing import Annotated

from fastapi import APIRouter, Body

from app.api.dependencies import SessionDep
from app.crud import create_db, delete_db, get_item_data, update_item
from app.dbmodels import Items
from app.schemas import ItemCreate, ItemPrivate, ItemPublic, ReturnMessage

router = APIRouter(prefix="/room", tags=["items"])


@router.post(
    "/{room_id}/item_create",
    # dependencies=[Depends(get_auth_user)],
    response_model=ItemPublic,
    response_description="Title and content of new item",
)
async def create_item(
    room_id: str,
    db: SessionDep,
    title: Annotated[str, Body(...)],
    content: Annotated[str, Body()] = "",
):
    item_priv = ItemCreate(title=title, content=content, room_id=room_id)
    data = Items(title=item_priv.title, content=item_priv.content, room_id=item_priv.room_id)
    item = create_db(db, data)
    return item


@router.get(
    "/{room_id}/{item_id}",
    # dependencies=[Depends(get_auth_user)],
    response_model=ItemPublic,
    response_description="Title and content of item",
)
async def view_item(
    room_id: str,
    item_id: int,
    db: SessionDep,
):
    item_priv = ItemPrivate(id=item_id, room_id=room_id)
    data = Items(id=item_priv.id, room_id=item_priv.room_id)
    item = get_item_data(db, data)
    return item


@router.put(
    "/{room_id}/{item_id}",
    # dependencies=[Depends(get_auth_user)],
    response_model=ItemPublic,
    response_description="Title and content of edited item",
)
async def edit_item(
    room_id: str,
    item_id: int,
    db: SessionDep,
    title: Annotated[str, Body(...)],
    content: Annotated[str, Body()] = "",
):
    priv = ItemPrivate(id=item_id, room_id=room_id)
    pub = ItemPublic(title=title, content=content)
    data = Items(id=priv.id, room_id=priv.room_id, title=pub.title, content=pub.content)
    item = update_item(db, data)
    return item


@router.delete(
    "/{room_id}/{item_id}",
    # dependencies=[Depends(get_auth_user)],
    response_model=ReturnMessage,
    response_description="Item deleted",
)
async def delete_item(room_id: str, item_id: int, db: SessionDep):
    priv = ItemPrivate(id=item_id, room_id=room_id)
    data = Items(id=priv.id, room_id=priv.room_id)
    result = delete_db(db, data)
    return result
