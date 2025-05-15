from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.color import Color

async def seed_brands(db: AsyncSession):
    colors = [
        Color(name="Красный"),
        Color(name="Синий"),
        Color(name="Зелёный"),
        Color(name="Чёрный"),
        Color(name="Белый"),
        Color(name="Жёлтый"),
        Color(name="Оранжевый"),
        Color(name="Фиолетовый"),
        Color(name="Розовый"),
        Color(name="Коричневый"),
        Color(name="Серый"),
    ]
    db.add_all(colors)
    await db.flush()
    await db.commit()
# обновить сиды таблицы sneakers
