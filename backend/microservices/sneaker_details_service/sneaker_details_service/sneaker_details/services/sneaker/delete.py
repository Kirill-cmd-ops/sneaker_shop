from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import (
    SneakerSizeAssociation,
    SneakerColorAssociation,
    SneakerMaterialAssociation,
    Sneaker,
)


async def delete_sneaker_service(session: AsyncSession, sneaker_id: int):
    assoc_tables = [
        SneakerSizeAssociation,
        SneakerColorAssociation,
        SneakerMaterialAssociation,
    ]

    async with session.begin():
        for assoc_table in assoc_tables:
            stmt = delete(assoc_table).where(assoc_table.sneaker_id == sneaker_id)
            await session.execute(stmt)

        stmt = delete(Sneaker).where(Sneaker.id == sneaker_id)
        await session.execute(stmt)
