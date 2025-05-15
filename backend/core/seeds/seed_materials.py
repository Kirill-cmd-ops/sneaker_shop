from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.material import Material

async def seed_materials(db: AsyncSession):
    materials = [
        Material(name="Сетка (Mesh)"),
        Material(name="Кожа"),
        Material(name="Замша"),
        Material(name="Нубук"),
        Material(name="Полиэстер"),
        Material(name="Эко-кожа"),
        Material(name="Текстиль"),
        Material(name="Спандекс"),
        Material(name="Резина"),
        Material(name="Phylon"),
        Material(name="TPU (Термополиуретан)"),
        Material(name="EVA"),
    ]

    db.add_all(materials)
    await db.commit()
