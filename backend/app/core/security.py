from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.exceptions import AuthenticationError, NotFoundError
from app.schemas import RoomPrivate, User, UserPrivate


class Authenticator:
    def __init__(
        self,
        secret_key: str = settings.jwt_secret_key,
        algorithm: str = settings.jwt_algorithm,
        expiration_time: int = settings.jwt_exp_time,
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
        except (NotFoundError, AuthenticationError) as e:
            raise AuthenticationError from e
        return user

    def authenticate_room(self, db: Session, room_id: str, room_pw: str) -> RoomPrivate:
        try:
            room = crud.get_room(db, room_id)
            self.verify_password(room_pw, room.password)
        except (NotFoundError, AuthenticationError) as e:
            raise AuthenticationError from e
        return room


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=settings.jwt_algorithm,
            options={
                "require_sub": True,
                "require_exp": True,
            },
        )
    except JWTError as e:
        raise AuthenticationError from e
    user_id = UUID(payload["sub"])
    return user_id


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    """Decode token -> Validate token -> Get user
    :returns: User ID (type UUID)"""
    user_id = decode_token(token)
    return user_id
