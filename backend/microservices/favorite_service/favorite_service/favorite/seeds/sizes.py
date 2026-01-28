from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from microservices.favorite_service.favorite_service.favorite.models import Size


async def seed_sizes(session: AsyncSession):
    sizes = [{"eu_size": size} for size in range(35, 47)]
    stmt = insert(Size).values(sizes)
    await session.execute(stmt)
    await session.commit()
