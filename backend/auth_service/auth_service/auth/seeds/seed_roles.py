from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.auth.models import Role


async def seed_roles(db: AsyncSession):
    await db.execute(
        insert(Role),
        [
            {"name": "user"},
            {"name": "content_manager"},
            {"name": "admin"},
        ],
    )

    await db.commit()

