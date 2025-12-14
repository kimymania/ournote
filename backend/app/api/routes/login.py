from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status

from app.api.dependencies import SessionDep
from app.core.security import hash_password
from app.crud import create_user, get_username_match
from app.models import Users as UserDB
from app.schemas import User, UserCreate

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=User, response_description="user added successfully")
async def signup(
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    db: SessionDep,
):
    result = get_username_match(db, username)
    if result is not None:
        return HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = UserCreate(username=username, password=hash_password(password))
    data = UserDB(username=user.username, password=user.password)
    user = create_user(db, data)
    return user
