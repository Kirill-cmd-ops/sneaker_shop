from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.size import Size

async def seed_sizes(db: AsyncSession):
    sizes = [Size(eu_size=size) for size in range(15, 51)]
    db.add_all(sizes)
    await db.commit()
