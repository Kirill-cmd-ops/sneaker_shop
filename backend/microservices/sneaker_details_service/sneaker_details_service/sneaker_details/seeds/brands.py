from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import Brand


async def seed_brands(session: AsyncSession):
    brands = [
        {"name": "Nike", "image_url": "/uploads/brands/nike.png"},
        {"name": "Adidas", "image_url": "/uploads/brands/adidas.png"},
        {"name": "Puma", "image_url": "/uploads/brands/puma.png"},
        {"name": "Vans", "image_url": "/uploads/brands/vans.png"},
        {"name": "Salomon", "image_url": "/uploads/brands/salomon.png"},
        {"name": "Asics", "image_url": "/uploads/brands/asics.png"},
        {"name": "New balance", "image_url": "/uploads/brands/newbalance.png"},
        {"name": "Reebok", "image_url": "/uploads/brands/reebok.png"},
        {"name": "Converse", "image_url": "/uploads/brands/converse.png"},
        {"name": "Jordan", "image_url": "/uploads/brands/jordan.png"},
        {"name": "Under Armour", "image_url": "/uploads/brands/underarmour.png"},
        {"name": "Saucony", "image_url": "/uploads/brands/saucony.png"},
        {"name": "Fila", "image_url": "/uploads/brands/fila.png"},

        {"name": "Hoka", "image_url": "/uploads/brands/hoka.png"},
        {"name": "Mizuno", "image_url": "/uploads/brands/mizuno.png"},
        {"name": "Diadora", "image_url": "/uploads/brands/diadora.png"},
        {"name": "Brooks", "image_url": "/uploads/brands/brooks.png"},
        {"name": "Kappa", "image_url": "/uploads/brands/kappa.png"},
    ]
    stmt = insert(Brand).values(brands)
    await session.execute(stmt)
    await session.commit()
