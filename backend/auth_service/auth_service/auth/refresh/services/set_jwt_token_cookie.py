from fastapi.openapi.models import Response
from fastapi_users import models

from auth_service.auth.authentication.custom_jwt import MyJWTStrategy
from auth_service.auth.config import settings
from auth_service.auth.refresh.utils.set_cookie import set_value_in_cookie


async def set_jwt_token(
    user_id: int | models.UP,
    token_aud: list[str],
    response: Response,
):
    strategy = MyJWTStrategy(
        secret=settings.auth_config.jwt_private_key,
        lifetime_seconds=settings.auth_config.lifetime_seconds,
        algorithm=settings.auth_config.algorithm,
        public_key=settings.auth_config.jwt_public_key,
        issuer=settings.auth_config.issuer,
        token_audience=token_aud,
        allowed_audience=settings.auth_config.allowed_audience,
    )
    access_token = await strategy.write_token(user_id)

    set_value_in_cookie(
        response,
        value=access_token,
        key=settings.cookie.jwt_cookie_name,
        max_age=settings.cookie.jwt_cookie_max_age,
        path=settings.cookie.cookie_path,
        secure=settings.cookie.cookie_secure,
        httponly=settings.cookie.cookie_httponly,
        samesite=settings.cookie.cookie_samesite,
    )