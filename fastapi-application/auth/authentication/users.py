from fastapi import APIRouter

from auth.authentication.fastapi_users import fastapi_users
from auth.config import settings
from auth.schemas.user import (
    UserRead,
    UserUpdate,
)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)