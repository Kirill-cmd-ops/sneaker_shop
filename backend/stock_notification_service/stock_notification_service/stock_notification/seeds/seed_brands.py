from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from stock_notification_service.stock_notification.models import Brand


async def seed_brands(session: AsyncSession):
    brands = [
        {"name": "Nike", "image_url": "/uploads/brands/nike.png"},
        {"name": "Adidas", "image_url": "/uploads/brands/adidas.png"},
        {"name": "Puma", "image_url": "/uploads/brands/puma.png"},
        {"name": "Vans", "image_url": "/uploads/brands/vans.png"},
        {"name": "Salomon", "image_url": "/uploads/brands/salomon.png"},
        {"name": "Asics", "image_url": "/uploads/brands/asics.png"},
        {"name": "New-balance", "image_url": "/uploads/brands/new-balance.png"},
    ]
    stmt = insert(Brand).values(brands)
    await session.execute(stmt)
    await session.commit()
