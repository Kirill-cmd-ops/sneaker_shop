from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.auth_service.auth_service.auth.models import Role


async def seed_roles(session: AsyncSession):
    roles = [
        {"name": "user"},
        {"name": "content_manager"},
        {"name": "admin"},
    ]

    stmt = insert(Role).values(roles)
    await session.execute(stmt)

    await session.commit()
