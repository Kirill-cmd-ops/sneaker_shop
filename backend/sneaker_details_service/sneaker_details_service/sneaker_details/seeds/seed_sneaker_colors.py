from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import (
    SneakerColorAssociation,
    Sneaker,
    Color,
)
import random


async def seed_sneaker_colors(session: AsyncSession):
    sneakers = (await session.execute(select(Sneaker))).scalars().all()
    colors = (await session.execute(select(Color))).scalars().all()

    associations = []

    for sneaker in sneakers:
        assigned_colors = random.sample(colors, min(3, len(colors)))

        for color in assigned_colors:
            associations.append({"sneaker_id": sneaker.id, "color_id": color.id})

    stmt = insert(SneakerColorAssociation).values(associations)
    await session.execute(stmt)
    await session.commit()
