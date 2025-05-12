from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.sneaker_size import SneakerSizeAssociation

async def seed_sneaker_sizes(db: AsyncSession):
    associations = []

    size_ids = [1, 2, 3, 4, 5]

    sneaker_ids = list(range(1, 33))

    for sneaker_id in sneaker_ids:
        for size_id in size_ids:
            quantity = (sneaker_id + size_id) % 10 + 1
            associations.append(SneakerSizeAssociation(sneaker_id=sneaker_id, size_id=size_id, quantity=quantity))

    db.add_all(associations)
    await db.flush()
    await db.commit()

