from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import Sneaker


async def seed_sneakers(db: AsyncSession):
    sneakers = [
        Sneaker(
            name="Air Max 90",
            description="Лучшие кросовки своей линейки",
            price=215.99,
            brand_id=1,
            country_id=1,
            gender="Женские",
            image_url="/uploads/sneakers/nike_air_max.png",
        )
    ]

    db.add_all(sneakers)
    await db.flush()
    await db.commit()
