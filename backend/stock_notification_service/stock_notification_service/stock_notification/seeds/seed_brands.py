from sqlalchemy.ext.asyncio import AsyncSession
from stock_notification_service.stock_notification.models import Brand

async def seed_brands(db: AsyncSession):
    brands = [
        Brand(name="Nike", image_url="/uploads/brands/nike.png"),
        Brand(name="Adidas", image_url="/uploads/brands/adidas.png"),
        Brand(name="Puma", image_url="/uploads/brands/puma.png"),
        Brand(name="Vans", image_url="/uploads/brands/vans.png"),
        Brand(name="Salomon", image_url="/uploads/brands/salomon.png"),
        Brand(name="Asics", image_url="/uploads/brands/asics.png"),
        Brand(name="New-balance", image_url="/uploads/brands/new-balance.png"),
    ]
    db.add_all(brands)
    await db.flush()
    await db.commit()
