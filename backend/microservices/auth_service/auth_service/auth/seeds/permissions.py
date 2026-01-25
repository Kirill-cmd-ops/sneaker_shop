from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import Permission


async def seed_permission(session: AsyncSession):
    permissions = [
        {"name": "favorite.view"},
        {"name": "favorite.sneaker.add"},
        {"name": "favorite.sneaker.delete"},
        {"name": "cart.view"},
        {"name": "cart.sneaker.add"},
        {"name": "cart.sneaker.update"},
        {"name": "cart.sneaker.delete"},
        {"name": "details.sneaker.create"},
        {"name": "details.sneaker.update"},
        {"name": "details.sneaker.delete"},
        {"name": "details.sneaker.size.view"},
        {"name": "details.sneaker.size.create"},
        {"name": "details.sneaker.size.update"},
        {"name": "details.sneaker.size.delete"},
        {"name": "details.sneaker.color.view"},
        {"name": "details.sneaker.color.create"},
        {"name": "details.sneaker.color.delete"},
        {"name": "details.sneaker.material.view"},
        {"name": "details.sneaker.material.create"},
        {"name": "details.sneaker.material.delete"},
    ]

    stmt = insert(Permission).values(permissions)
    await session.execute(stmt)
    await session.commit()
