from fastapi import APIRouter

from auth_service.auth.authentication.routers import router as auth_router
from auth_service.auth.authentication.users import router as users_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
