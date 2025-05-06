from fastapi import APIRouter

from core.authentication.routers import router as auth_router
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(auth_router)