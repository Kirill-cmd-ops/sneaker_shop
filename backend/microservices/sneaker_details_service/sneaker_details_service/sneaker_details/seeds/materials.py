from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import Material


async def seed_materials(session: AsyncSession):
    materials = [
        {"name": "Сетка (Mesh)"},
        {"name": "Кожа"},
        {"name": "Замша"},
        {"name": "Нубук"},
        {"name": "Полиэстер"},
        {"name": "Эко-кожа"},
        {"name": "Текстиль"},
        {"name": "Спандекс"},
        {"name": "Резина"},
        {"name": "Phylon"},
        {"name": "TPU (Термополиуретан)"},
        {"name": "EVA"},
        {"name": "Canvas"},
        {"name": "Flyknit"},
        {"name": "Primeknit"},
    ]
    stmt = insert(Material).values(materials)
    await session.execute(stmt)
    await session.commit()
