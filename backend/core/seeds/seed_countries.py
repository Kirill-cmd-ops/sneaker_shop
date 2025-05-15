from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.models.country import Country

async def seed_brands(db: AsyncSession):
    countries = [
        Country(name="Argentina"),
        Country(name="China"),
        Country(name="France"),
        Country(name="Georgia"),
        Country(name="Germany"),
        Country(name="Italy"),
        Country(name="Latvia"),
        Country(name="Lithuania"),
        Country(name="Poland"),
        Country(name="Portugal"),
        Country(name="Spain"),
    ]
    db.add_all(countries)
    await db.flush()
    await db.commit()
# обновить сиды таблицы sneakers