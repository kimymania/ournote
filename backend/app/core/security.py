from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from uuid import UUID

from app import crud
from app.exceptions import AuthenticationError, NotFoundError
from app.schemas import RoomPrivate, User, UserPrivate
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

# Temporary
SECRET_KEY = "9A2D253F008E9667ECE093F3C427CC8689107B3299172E3C5DE0DF65AA24125E"
ALGORITHM = "HS256"
EXPIRATION_TIME = 15


class Authenticator:
    def __init__(
        self,
        secret_key: str = SECRET_KEY,
        algorithm: str = "HS256",
        expiration_time: int = 15,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_time = expiration_time
        self.password_hash = PasswordHash.recommended()

    def verify_password(self, password: str, hash: str) -> bool:
        verify = self.password_hash.verify(password, hash)
        if not verify:
            raise AuthenticationError
        return True

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def create_access_token(self, user_id: UUID) -> str:
        exp = timedelta(minutes=self.expiration_time)
        now = datetime.now(tz=timezone.utc)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + exp,
        }
        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def authenticate_user(self, db: Session, input: User) -> UserPrivate:
        try:
            user = crud.get_user_by_username(db, input.username)
            self.verify_password(input.password, user.password)
        except NotFoundError, AuthenticationError:
            raise AuthenticationError
        return user

    def authenticate_room(self, db: Session, room_id: str, password: str) -> RoomPrivate:
        try:
            room = crud.get_room(db, room_id)
            self.verify_password(password, room.password)
        except NotFoundError, AuthenticationError:
            raise AuthenticationError
        return room


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_token(payload: dict[str, Any]) -> UUID:
    try:
        user_id_str: str = payload["sub"]
        user_id = UUID(user_id_str)
    except KeyError:
        raise AuthenticationError(detail="Invalid token")
    except (ValueError, AttributeError):
        raise AuthenticationError(detail="Invalid token")

    try:
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    except KeyError:
        raise AuthenticationError(detail="Invalid token")
    if exp < datetime.now(timezone.utc):
        raise AuthenticationError(detail="Token expired")

    return user_id


def decode_token(token: str) -> UUID:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError as e:
        raise e
    return validate_token(payload)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    """Decode token -> Validate token -> Get user
    :returns: User ID (type UUID)"""
    user_id = decode_token(token)
    return user_id
