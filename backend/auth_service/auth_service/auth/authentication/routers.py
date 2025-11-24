from fastapi import APIRouter

from auth_service.auth.authentication.backends import auth_backend
from auth_service.auth.authentication.fastapi_users_custom import FastAPIUsersCustom
from auth_service.auth.refresh.routers.refresh_routers import refresh_router
from auth_service.auth.dependencies.user_manager import get_user_manager
from auth_service.auth.schemas import UserRead, UserCreate

from auth_service.auth.authentication.oauth import google_oauth_client
from auth_service.auth.config import settings


fastapi_users_custom = FastAPIUsersCustom(
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Auth"],
)

router.include_router(
    fastapi_users_custom.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users_custom.get_register_router(
        UserRead,
        UserCreate,
    ),
)

router.include_router(
    fastapi_users_custom.get_verify_router(UserRead),
)


router.include_router(
    fastapi_users_custom.get_reset_password_router(),
)

router.include_router(
    fastapi_users_custom.get_oauth_router(
        google_oauth_client,
        auth_backend,
        settings.auth_config.state_secret,
        associate_by_email=True,
    ),
)

router.include_router(
    fastapi_users_custom.get_oauth_associate_router(
        google_oauth_client,
        UserRead,
        settings.auth_config.state_secret,
    ),
)

router.include_router(refresh_router)