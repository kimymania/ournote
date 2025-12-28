from fastapi import APIRouter

from .routes.auth import router as auth

# from .routes.items import router as items
from .routes.rooms import router as rooms
from .routes.user import router as user

router = APIRouter()
router.include_router(auth)
router.include_router(user)
router.include_router(rooms)
# router.include_router(items)
