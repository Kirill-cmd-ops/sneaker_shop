from fastapi import APIRouter

from auth.authentication.routers import router as auth_router
from auth.authentication.users import router as users_router
from core.routers.sneaker import router as sneaker_router
from auth.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(auth_router)

router.include_router(users_router)

router.include_router(sneaker_router)