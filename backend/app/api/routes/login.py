"""Sign up, sign in, password reset"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from pydantic import Field

from app.api.dependencies import SessionDep, get_auth_user
from app.cache import get_id_by_username, remove_session, store_session
from app.core.security import generate_session_id, hash_password
from app.crud import authenticate_user, create_db, get_username_match
from app.dbmodels import Users as UserDB
from app.schemas import ReturnMessage, UserCreate, UsernameRule, UserPrivate, UserPublic

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=UserPublic, response_description="user added successfully")
async def signup(
    username: Annotated[str, Form(...), UsernameRule],
    password: Annotated[str, Form(...), Field(min_length=8, max_length=16)],
    db: SessionDep,
):
    # try:
    user = UserCreate(username=username, password=hash_password(password))
    # except ValidationError:
    #     raise HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    #         detail="username doesn't match conventions",
    #     )
    if get_username_match(db, user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    data = UserDB(username=user.username, password=user.password)
    user = create_db(db, data)
    return user


@router.post("/login", response_model=UserPublic, response_description="login successful")
async def login(
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    session_id: Annotated[str, Depends(generate_session_id)],
    db: SessionDep,
    response: Response,
):
    user_id = get_id_by_username(username)
    credentials = UserPrivate(id=user_id, username=username, password=password)
    result = authenticate_user(db, credentials)
    response.set_cookie(
        key="Authorization",
        value=session_id,
        max_age=60 * 30,  # 30 minute max
        httponly=True,
        secure=True,
    )

    await store_session(session_id, result.id)
    user = UserPublic(username=username)

    return user


@router.post(
    "/logout",
    response_model=ReturnMessage,
    response_description="log out result",
)
async def logout(
    session_id: Annotated[str, Depends(get_auth_user)],
    response: Response,
):
    await remove_session(session_id)
    response.delete_cookie(key="Authorization")
    return ReturnMessage(msg="logged out")
