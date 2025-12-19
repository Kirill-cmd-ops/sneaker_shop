from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import Country


async def seed_countries(session: AsyncSession):
    countries = [
        {"name": "Argentina"},
        {"name": "China"},
        {"name": "France"},
        {"name": "Georgia"},
        {"name": "Germany"},
        {"name": "Italy"},
        {"name": "Latvia"},
        {"name": "Lithuania"},
        {"name": "Poland"},
        {"name": "Portugal"},
        {"name": "Spain"},
    ]
    stmt = insert(Country).values(countries)
    await session.execute(stmt)
    await session.commit()
