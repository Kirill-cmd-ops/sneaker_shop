from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.size import Size

async def seed_sizes(db: AsyncSession):
    sizes = [Size(eu_size=size) for size in [38.0, 40.5, 42.0, 44.5, 46.0]]
    db.add_all(sizes)
    await db.commit()  # Асинхронный коммит

