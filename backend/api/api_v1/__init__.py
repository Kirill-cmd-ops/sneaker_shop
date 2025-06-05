from fastapi import APIRouter

from backend.core.routers.sneakers import router as sneakers_router
from backend.core.routers.sneaker import router as sneaker_router
from auth_service.auth.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(sneakers_router)

router.include_router(sneaker_router)
