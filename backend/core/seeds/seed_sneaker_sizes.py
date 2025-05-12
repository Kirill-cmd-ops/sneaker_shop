from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.sneaker_size import SneakerSizeAssociation

async def seed_sneaker_sizes(db: AsyncSession):
    associations = [
        SneakerSizeAssociation(sneaker_id=1, size_id=1, quantity=5),
        SneakerSizeAssociation(sneaker_id=1, size_id=2, quantity=3),
        SneakerSizeAssociation(sneaker_id=2, size_id=3, quantity=6),
        #
        SneakerSizeAssociation(sneaker_id=3, size_id=4, quantity=1),
        SneakerSizeAssociation(sneaker_id=4, size_id=5, quantity=12),
        SneakerSizeAssociation(sneaker_id=5, size_id=1, quantity=54),
        SneakerSizeAssociation(sneaker_id=6, size_id=3, quantity=9),
    ]
    db.add_all(associations)
    await db.flush()  # Фиксируем добавленные объекты
    await db.commit()  # Асинхронный коммит
