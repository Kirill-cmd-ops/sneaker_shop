from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import RefreshToken


async def hash_refresh_token_add_db(
    session: AsyncSession, refresh_token: str, user_id: int
):
    token = RefreshToken(
        user_id=user_id,
        token_hash=refresh_token,
        expires_at=datetime.utcnow() + timedelta(weeks=4),
    )
    session.add(token)
    await session.commit()
