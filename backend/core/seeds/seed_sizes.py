from sqlalchemy.ext.asyncio import AsyncSession
from backend.catalog_service.catalog_service.catalog.models import Size

async def seed_sizes(db: AsyncSession):
    sizes = [Size(eu_size=size) for size in range(15, 51)]
    db.add_all(sizes)
    await db.commit()
