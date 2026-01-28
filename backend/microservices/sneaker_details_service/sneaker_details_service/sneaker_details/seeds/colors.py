from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import Color


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
        {"name": "Бежевый"},
        {"name": "Хаки"},
        {"name": "Бирюзовый"},
        {"name": "Металлик"},
        {"name": "Золотой"},
        {"name": "Серебряный"},
        {"name": "Бордовый"},
        {"name": "Лаймовый"},
        {"name": "Аквамарин"},
        {"name": "Небесно-голубой"},
        {"name": "Оливковый"},
    ]
    stmt = insert(Color).values(colors)
    await session.execute(stmt)
    await session.commit()
