from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.auth_service.auth_service.auth.models import db_helper, RefreshToken


async def get_refresh_token_id(
        hash_refresh_token,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await session.scalar(
        select(RefreshToken.id).where(RefreshToken.token_hash == hash_refresh_token)
    )
