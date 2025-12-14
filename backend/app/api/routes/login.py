from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status

from app.api.dependencies import SessionDep
from app.core.security import generate_session_id, hash_password
from app.crud import authenticate_user, create_user, get_username_match
from app.models import Users as UserDB
from app.schemas import User, UserCreate, UserLogin

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=User, response_description="user added successfully")
async def signup(
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    db: SessionDep,
):
    if get_username_match(db, username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = UserCreate(username=username, password=hash_password(password))
    data = UserDB(username=user.username, password=user.password)
    user = create_user(db, data)
    return user


@router.post("/login", response_model=User, response_description="login successful")
async def login(
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    session_id: Annotated[str, Depends(generate_session_id)],
    db: SessionDep,
    response: Response,
):
    credentials = UserLogin(username=username, password=password)
    user = authenticate_user(db, credentials)
    response.set_cookie(
        key="Authorization",
        value=session_id,
        max_age=60 * 30,  # 30 minute max
        httponly=True,
        secure=True,
    )
    return user
