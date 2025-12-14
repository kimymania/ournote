from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Users
from app.schemas import User


def get_username_match(db: Session, username: str) -> bool:
    query = db.get(Users, username)
    if query is None:
        return False
    return True


def create_user(db: Session, data: Users) -> User:
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        user = User(username=data.username)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise e
