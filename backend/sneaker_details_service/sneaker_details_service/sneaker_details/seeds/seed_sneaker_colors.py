from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.catalog_service.catalog_service.catalog.models import SneakerColorAssociation
from backend.catalog_service.catalog_service.catalog.models import Sneaker
from backend.catalog_service.catalog_service.catalog.models import Color
import random

async def seed_sneaker_colors(db: AsyncSession):
    sneakers = (await db.execute(select(Sneaker))).scalars().all()
    colors = (await db.execute(select(Color))).scalars().all()

    associations = []

    for sneaker in sneakers:
        assigned_colors = random.sample(colors, min(3, len(colors)))

        for color in assigned_colors:
            associations.append(
                SneakerColorAssociation(sneaker_id=sneaker.id, color_id=color.id)
            )

    db.add_all(associations)
    await db.commit()
