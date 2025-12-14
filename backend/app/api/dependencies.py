from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.cache import SESSION_DB
from app.core.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]


def get_auth_user(request: Request) -> str:
    """Authorization Dependency: Verify that user has a valid session"""
    session_id = request.cookies.get("Authorization")
    if not session_id:  # not authenticated
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif session_id not in SESSION_DB:  # not authorized
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return session_id
