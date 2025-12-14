from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_user

router = APIRouter(tags=["user"])


@router.get("/{username}", dependencies=[Depends(get_auth_user)])
async def user_home(username: str):
    pass
