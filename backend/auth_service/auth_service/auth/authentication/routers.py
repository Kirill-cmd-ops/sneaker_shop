from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from auth_service.auth.authentication.backends import auth_backend
from auth_service.auth.config import settings
from auth_service.auth.dependencies.user_manager import get_user_manager
from auth_service.auth.models import User
from auth_service.auth.schemas.user import UserRead, UserCreate
from auth_service.auth.types.user_id import UserIdType

from auth_service.auth.authentication.oauth import google_oauth_client
from auth_service.auth.config import settings

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

router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        settings.auth_config.state_secret,
        associate_by_email=True,
    ),
)

router.include_router(
    fastapi_users.get_oauth_associate_router(
        google_oauth_client,
        UserRead,
        settings.auth_config.state_secret,
    ),
)
