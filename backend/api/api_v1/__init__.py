from fastapi import APIRouter

from backend.auth.authentication.routers import router as auth_router
from backend.auth.authentication.users import router as users_router
from backend.core.routers.sneakers import router as sneakers_router
from backend.core.routers.sneaker import router as sneaker_router
from backend.auth.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(auth_router)

router.include_router(users_router)

router.include_router(sneakers_router)

router.include_router(sneaker_router)