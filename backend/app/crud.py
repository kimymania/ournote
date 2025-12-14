from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Users


def get_username_match(username: str, db: Session) -> bool:
    query = db.get(Users, username)
    if query is None:
        return False
    return True


def create_db(data: Any, db: Session) -> None:
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
