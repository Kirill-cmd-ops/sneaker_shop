import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import (
    SneakerSizeAssociation,
    Sneaker,
    Size,
)


async def seed_sneaker_sizes(db: AsyncSession):
    sneakers = (await db.execute(select(Sneaker))).scalars().all()
    sizes = (await db.execute(select(Size))).scalars().all()

    associations = []

    for sneaker in sneakers:
        assigned_sizes = random.sample(sizes, min(3, len(sizes)))

        for size in assigned_sizes:
            quantity = random.randint(1, 10)
            associations.append(
                SneakerSizeAssociation(
                    sneaker_id=sneaker.id, size_id=size.id, quantity=quantity
                )
            )

    db.add_all(associations)
    await db.flush()
    await db.commit()
