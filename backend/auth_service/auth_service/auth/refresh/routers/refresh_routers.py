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
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.refresh,
    ),
    tags=["Refresh Token"],
)


@refresh_router.post("/")
async def all_logic_refresh_token(
    response: Response,
    token_aud: list[str],
    session: AsyncSession = Depends(db_helper.session_getter),
    refresh_token: str = Cookie(alias="refresh_session_cookie"),
):
    async with session.begin():
        # 1) Проверка refresh токена
        user_id = await check_refresh_token_valid(
            session=session,
            refresh_token=refresh_token,
        )

    # 2) Создание нового access токена и прокид в cookie
    await set_jwt_token(
        user_id=user_id,
        token_aud=token_aud,
        response=response,
    )

    # 3) Создание нового refresh токена
    raw = secrets.token_bytes(32)
    new_refresh_token = generate_refresh_token(raw)

    # 4) Хэшируем старый refresh токен, перед созданием нового
    hash_old_token = encode_refresh_token(refresh_token=refresh_token)

    # 5) Хеширование нового refresh токена
    hash_new_token = encode_refresh_token(refresh_token=new_refresh_token)

    async with session.begin():
        # 6) Получаем jti старого refresh токена, для добавления в blacklist
        refresh_token_id = await get_refresh_token_id(
            hash_refresh_token=hash_old_token,
            session=session,
        )

        # 7) Добавление в blacklist старого refresh токена
        await add_to_blacklist(session=session, refresh_token_id=refresh_token_id)

        # 8) Добавление нового refresh токена в бд
        await hash_refresh_token_add_db(
            session=session,
            refresh_token=hash_new_token,
            user_id=user_id,
        )

    # 9) Записываем refresh токен в cookie
    set_value_in_cookie(
        response=response,
        value=new_refresh_token,
        key=settings.cookie.refresh_cookie_name,
        max_age=settings.cookie.refresh_cookie_max_age,
        path=settings.cookie.cookie_path,
        secure=settings.cookie.cookie_secure,
        httponly=settings.cookie.cookie_httponly,
        samesite=settings.cookie.cookie_samesite,
    )

    return {"result": "ok"}
