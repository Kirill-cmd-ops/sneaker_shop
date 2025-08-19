from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import db_helper, RefreshToken


async def get_refresh_token_id(
    hash_refresh_token,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(RefreshToken.id).where(RefreshToken.token_hash == hash_refresh_token)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
