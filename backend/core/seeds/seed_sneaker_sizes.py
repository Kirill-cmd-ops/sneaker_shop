import random
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.sneaker_size import SneakerSizeAssociation

async def seed_sneaker_sizes(db: AsyncSession):
    associations = []

    sneaker_ids = list(range(1, 33))

    for sneaker_id in sneaker_ids:
        size_ids = sorted(random.sample(range(1, 37), k=random.randint(2, 5)))

        for size_id in size_ids:
            quantity = random.randint(1, 10)
            associations.append(SneakerSizeAssociation(sneaker_id=sneaker_id, size_id=size_id, quantity=quantity))

    db.add_all(associations)
    await db.flush()
    await db.commit()
