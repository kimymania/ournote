import secrets
from uuid import UUID

from pwdlib import PasswordHash

SESSION_DB = {}
password_hash = PasswordHash.recommended()


def verify_password(password: str, hash: str) -> bool:
    return password_hash.verify(password, hash)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def generate_session_id() -> str:
    return secrets.token_urlsafe(32)


def store_session_id(session_id: str, user_id: UUID) -> None:
    SESSION_DB[session_id] = user_id
