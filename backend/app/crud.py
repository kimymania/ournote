from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Users
from app.schemas import User


def get_username_match(db: Session, username: str) -> bool:
    stmt = select(Users).where(Users.username == username)
    result = db.execute(stmt).scalar_one_or_none()
    if result is None:
        return False
    return True


def create_user(db: Session, data: Users) -> User:
    try:
        user = User(username=data.username)
        db.add(data)
        db.commit()
        db.refresh(data)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise e
