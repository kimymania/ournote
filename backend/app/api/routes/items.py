from typing import Annotated

from fastapi import APIRouter, Body
from starlette import status
from starlette.responses import Response

from app.api.dependencies import SessionDep
from app.exceptions import DBError, DuplicateDataError, NotFoundError
from app.schemas import Item
from app.services import items as service

router = APIRouter(prefix="/room", tags=["items"])


@router.post("/{room_id}/item/create", response_class=Response)
async def create_item(
    room_id: str,
    db: SessionDep,
    title: Annotated[str, Body(...)],
    content: Annotated[str | None, Body()] = None,
):
    result = await service.create_item(
        room_id=room_id,
        title=title,
        content=content,
        db=db,
    )
    if result.success:
        return Response(status_code=status.HTTP_201_CREATED)
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
    content: Annotated[str, Body()] = "",
):
    result = await service.edit_item(
        room_id=room_id,
        item_id=item_id,
        title=title,
        content=content,
        db=db,
    )
    if result:
        return result
    raise NotFoundError


@router.delete("/{room_id}/item/{item_id}", response_class=Response)
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
        return Response(status_code=status.HTTP_200_OK)
    raise DBError
