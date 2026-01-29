from fastapi import APIRouter

from microservices.auth_service.auth_service.auth.authentication.routers import router as auth_router
from microservices.auth_service.auth_service.auth.refresh.routers.refresh_routers import refresh_router
from microservices.auth_service.auth_service.auth.routers.role_permissions import router as role_permissions_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(role_permissions_router)
router.include_router(refresh_router)
