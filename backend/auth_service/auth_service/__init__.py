from fastapi import APIRouter

from auth_service.auth.authentication.routers import router as auth_router
from auth_service.auth.routers.role_permissions import router as role_permissions_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(role_permissions_router)
