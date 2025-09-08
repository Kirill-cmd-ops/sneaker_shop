from fastapi import APIRouter

from auth_service.auth.authentication.fastapi_users import fastapi_users
from auth_service.auth.config import settings
from auth_service.auth.schemas import (
    UserRead,
    UserUpdate,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.users,
    ),
    tags=["Users"],
)

router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
