from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import AuthDep, SessionDep
from app.schemas import Result, Token
from app.services import user
from app.services.rooms import generate_room_id

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token, response_description="JWT access token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: AuthDep,
    db: SessionDep,
):
    result = await user.login(form_data=form_data, auth=auth, db=db)
    data = result.data
    if data and isinstance(data, str):
        access_token = data
        return Token(access_token=access_token)


@router.get("/room_id", response_model=Result, response_description="Generated Room ID")
async def generate_id():
    result = generate_room_id()
    return result
