from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from microservices.auth_service.auth_service.auth.models import Blacklist


async def add_to_blacklist(
        session: AsyncSession,
        refresh_token_id,
):
    blacklist = Blacklist(
        refresh_token_id=refresh_token_id,
        revoked_at=datetime.utcnow(),
    )
    session.add(blacklist)
