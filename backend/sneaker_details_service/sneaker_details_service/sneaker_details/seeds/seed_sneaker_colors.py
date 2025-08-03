from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import SneakerColorAssociation
from sneaker_details_service.sneaker_details.models import Sneaker
from sneaker_details_service.sneaker_details.models import Color
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
