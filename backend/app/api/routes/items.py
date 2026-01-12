from typing import Annotated

from fastapi import APIRouter, Body

from app.api.dependencies import SessionDep
from app.exceptions import DBError, DuplicateDataError, NotFoundError
from app.schemas import Item
from app.services import items as service

router = APIRouter(prefix="/room", tags=["items"])


@router.post("/{room_id}/item/create", status_code=201)
async def create_item(
    room_id: str,
    db: SessionDep,
    title: Annotated[str, Body(...)],
    content_json: Annotated[list, Body(...)],
):
    result = await service.create_item(
        room_id=room_id,
        title=title,
        content_json=content_json,
        db=db,
    )
    if result.success:
        return
    raise DuplicateDataError


@router.get("/{room_id}/item/{item_id}", response_model=Item)
async def view_existing_item(
    room_id: str,
    item_id: int,
    db: SessionDep,
):
    result = await service.view_existing_item(
        room_id=room_id,
        item_id=item_id,
        db=db,
    )
    if result:
        return result
    raise NotFoundError


@router.put("/{room_id}/item/{item_id}", response_model=Item)
async def edit_item(
    room_id: str,
    item_id: int,
    db: SessionDep,
    title: Annotated[str, Body(...)],
    content_json: Annotated[list, Body(...)],
):
    result = await service.edit_item(
        room_id=room_id,
        item_id=item_id,
        title=title,
        content_json=content_json,
        db=db,
    )
    if result:
        return result
    raise NotFoundError


@router.delete("/{room_id}/item/{item_id}", status_code=200)
async def delete_item(
    room_id: str,
    item_id: int,
    db: SessionDep,
):
    result = await service.delete_item(
        room_id=room_id,
        item_id=item_id,
        db=db,
    )
    if result.success:
        return
    raise DBError
