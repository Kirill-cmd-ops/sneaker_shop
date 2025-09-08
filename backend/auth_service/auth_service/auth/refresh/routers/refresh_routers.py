import secrets

from fastapi import APIRouter
from fastapi.params import Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from auth_service.auth.config import settings

from auth_service.auth.models import db_helper
from auth_service.auth.refresh.dependencies.get_token_id import get_refresh_token_id
from auth_service.auth.refresh.services.add_token_in_blacklist import add_to_blacklist
from auth_service.auth.refresh.services.add_token_in_db import hash_refresh_token_add_db
from auth_service.auth.refresh.services.refresh_checks import check_refresh_token_valid
from auth_service.auth.refresh.services.set_jwt_token_cookie import set_jwt_token
from auth_service.auth.refresh.utils.encode_token import encode_refresh_token
from auth_service.auth.refresh.utils.generate_token import generate_refresh_token
from auth_service.auth.refresh.utils.set_cookie import set_value_in_cookie

refresh_router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.v1.refresh,
    )
)


@refresh_router.post("/refresh")
async def all_logic_refresh_token(
    response: Response,
    token_aud: list[str],
    session: AsyncSession = Depends(db_helper.session_getter),
    refresh_token: str = Cookie(alias="refresh_session_cookie"),
):

    # 1) Проверка refresh токена
    user_id = await check_refresh_token_valid(session, refresh_token)

    # 2) Создание нового access токена и прокид в cookie
    await set_jwt_token(user_id, token_aud, response)

    # 3) Хэшируем старый refresh токен, перед созданием нового
    hash_refresh_token = encode_refresh_token(refresh_token)

    # 4) Получаем jti refresh токена, для добавления в blacklist
    refresh_token_id = await get_refresh_token_id(hash_refresh_token, session)

    # 5) Добавление в blacklist
    await add_to_blacklist(session, refresh_token_id)

    # 6) Создание нового refresh токена
    raw = secrets.token_bytes(32)
    refresh_token = generate_refresh_token(raw)

    # 7) Записываем refresh токен в cookie
    set_value_in_cookie(
        response,
        value=refresh_token,
        key=settings.cookie.refresh_cookie_name,
        max_age=settings.cookie.refresh_cookie_max_age,
        path=settings.cookie.cookie_path,
        secure=settings.cookie.cookie_secure,
        httponly=settings.cookie.cookie_httponly,
        samesite=settings.cookie.cookie_samesite,
    )

    # 7) Хеширование refresh токена
    hash_refresh_token = encode_refresh_token(refresh_token)
    await hash_refresh_token_add_db(session, hash_refresh_token, user_id)

    return {"result": "ok"}
    # Просмотреть логику и подумать
