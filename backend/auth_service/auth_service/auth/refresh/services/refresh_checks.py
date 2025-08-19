from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models.refresh_token import RefreshToken
from auth_service.auth.refresh.utils.encode_token import encode_refresh_token


async def check_refresh_token_valid_rotation(session: AsyncSession, token_hash, rotate: bool = False, extra_days: int = 0):
    if rotate and extra_days > 0:
        stmt = select(RefreshToken.user_id).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked.is_(False),
            RefreshToken.expires_at > (datetime.utcnow() + timedelta(days=extra_days))
        )
    else:
        stmt = select(RefreshToken.user_id).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked.is_(False),
            RefreshToken.expires_at > datetime.utcnow(),
        )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def check_refresh_token_valid(session: AsyncSession, refresh_token: str):
    token_hash = encode_refresh_token(refresh_token)
    user_id = await check_refresh_token_valid_rotation(session, token_hash)
    if user_id is None:
        print("У данного пользователя нету рабочего refresh tokenа")
        return None
    return user_id


async def check_refresh_token_rotation(session: AsyncSession, refresh_token: str):
    token_hash = encode_refresh_token(refresh_token)
    user_id = await check_refresh_token_valid_rotation(session, token_hash, True, 5)
    if user_id is None:
        print("У данного пользователя почти истек токен")
        return None
    return user_id