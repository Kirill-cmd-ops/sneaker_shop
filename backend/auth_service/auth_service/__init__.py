from fastapi import APIRouter

from auth.authentication.routers import router as auth_router
from auth.authentication.users import router as users_router

router = APIRouter()


router.include_router(auth_router)
router.include_router(users_router)