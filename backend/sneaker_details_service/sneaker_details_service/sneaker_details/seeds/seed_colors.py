from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import Color


async def seed_colors(session: AsyncSession):
    colors = [
        {"name": "Красный"},
        {"name": "Синий"},
        {"name": "Зелёный"},
        {"name": "Чёрный"},
        {"name": "Белый"},
        {"name": "Жёлтый"},
        {"name": "Оранжевый"},
        {"name": "Фиолетовый"},
        {"name": "Розовый"},
        {"name": "Коричневый"},
        {"name": "Серый"},
    ]
    stmt = insert(Color).values(colors)
    await session.execute(stmt)
    await session.commit()
