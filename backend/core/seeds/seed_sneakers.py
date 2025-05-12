from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models.sneaker import Sneaker

async def seed_sneakers(db: AsyncSession):
    sneakers = [
        Sneaker(name="Air Max 90", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_air_max.jpg"),
        Sneaker(name="Ultraboost", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_ultraboost.jpg"),
        Sneaker(name="RS-X", description="Современный стиль", price=555.12, brand_id=3, image_url="/uploads/sneakers/puma_rs_x.jpg"),
        Sneaker(name="XT6", description="Для трейлраннинга", price=155.30, brand_id=4, image_url="/uploads/sneakers/salomon_xt6.jpg"),
        Sneaker(name="Gel-Kayano-30", description="Удобство и поддержка", price=229.60, brand_id=5, image_url="/uploads/sneakers/asics_gel_kayano_30.jpg"),
        Sneaker(name="2000", description="Классика", price=111.11, brand_id=6, image_url="/uploads/sneakers/new_balance_2000.jpg"),
    ]
    db.add_all(sneakers)
    await db.flush()
    await db.commit()

