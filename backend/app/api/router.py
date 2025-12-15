from fastapi import APIRouter

from .routes.login import router as login
from .routes.rooms import router as rooms
from .routes.user import router as user

router = APIRouter()
router.include_router(login)
router.include_router(user)
router.include_router(rooms)
