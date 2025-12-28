from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.core.security import Authenticator


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
AuthDep = Annotated[Authenticator, Depends()]
