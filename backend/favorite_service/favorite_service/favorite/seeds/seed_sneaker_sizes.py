import random
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from favorite_service.favorite.models import SneakerSizeAssociation, Sneaker, Size


async def seed_sneaker_sizes(session: AsyncSession):
    sneakers = (await session.execute(select(Sneaker))).scalars().all()
    sizes = (await session.execute(select(Size))).scalars().all()

    associations = []

    for sneaker in sneakers:
        assigned_sizes = random.sample(sizes, min(3, len(sizes)))

        for size in assigned_sizes:
            quantity = random.randint(1, 10)
            associations.append(
                {"sneaker_id": sneaker.id, "size_id": size.id, "quantity": quantity}
            )

    stmt = insert(SneakerSizeAssociation).values(associations)
    await session.execute(stmt)
    await session.commit()
