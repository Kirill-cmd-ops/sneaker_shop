from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from backend.auth.authentication.backends import auth_backend
from backend.auth.config import settings
from backend.auth.dependencies.user_manager import get_user_manager
from backend.auth.models import User
from backend.auth.schemas.user import UserRead, UserCreate
from backend.auth.types.user_id import UserIdType

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

router.include_router(
    router=fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)


router.include_router(
    fastapi_users.get_reset_password_router(),
)