from fastapi import APIRouter

from backend.auth_service.auth_service.auth.authentication.routers import router as auth_router
from backend.auth_service.auth_service.auth.authentication.users import router as users_router

router = APIRouter()


router.include_router(auth_router)
router.include_router(users_router)