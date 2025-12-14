from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import hash_password
from app.crud import create_db, get_username_match
from app.models import Users as UserDB
from app.schemas import UserCreate

router = APIRouter(tags=["login"])


@router.post("/signup")
async def create_user(
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    db: Annotated[Session, Depends(get_db)],
):
    result = get_username_match(username, db)
    if result is not None:
        return HTTPException(status_code=status.HTTP_409_CONFLICT)

    user = UserCreate(username=username, password=hash_password(password))
    data = UserDB(username=user.username, password=user.password)
    create_db(data, db)
    return {"status": 303, "detail": "user created"}
