from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import Authenticator
from app.crud import create_db, delete_db, get_user_by_id, get_user_by_username, get_user_rooms
from app.dbmodels import Users as UserDB
from app.exceptions import AuthenticationError, NotFoundError
from app.schemas import Result, RoomsList, User, UserCreate


async def create_user(
    username: str,
    password: str,
    db: Session,
    auth: Authenticator,
) -> Result:
    """:returns: UserPublic model containing username and empty list of rooms"""
    new_user = UserCreate(username=username, password=auth.hash_password(password))
    try:
        if get_user_by_username(db, new_user.username):
            return Result(success=False, detail="username already exists")
    except NotFoundError:
        pass

    data = UserDB(**new_user.model_dump(), rooms=[])
    result = create_db(db, data)
    return result


async def login(
    form_data: OAuth2PasswordRequestForm,
    auth: Authenticator,
    db: Session,
) -> Result:
    """:returns: access token string"""
    input = User(username=form_data.username, password=form_data.password)
    user = auth.authenticate_user(db=db, input=input)
    access_token = auth.create_access_token(user.id)
    result = Result(detail="successfully created token", data=access_token)
    return result


async def get_user_home(
    user_id: UUID,
    username: str,
    db: Session,
) -> RoomsList:
    user = get_user_by_id(db, user_id)
    if username != user.username:  # in case token doesn't match username url
        raise AuthenticationError
    rooms = get_user_rooms(db, user.id)
    return rooms


async def delete_user(
    user_id: UUID,
    auth: Authenticator,
    password: str,
    db: Session,
) -> Result:
    user = get_user_by_id(db, user_id)
    if not auth.verify_password(password, user.password):
        raise AuthenticationError(detail="wrong password")
    result = delete_db(db, user.id)
    return result
