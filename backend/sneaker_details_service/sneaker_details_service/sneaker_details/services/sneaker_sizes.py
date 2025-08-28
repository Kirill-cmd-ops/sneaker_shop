from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.schemas.sneaker_sizes import SneakerSizesCreate, SneakerSizesDelete

from sneaker_details_service.sneaker_details.models import SneakerSizeAssociation


async def create_sneaker_sizes(session: AsyncSession, sneaker_sizes_create: SneakerSizesCreate):
    for size_data in sneaker_sizes_create.sizes:
        sneaker_size = SneakerSizeAssociation(
            sneaker_id=sneaker_sizes_create.sneaker_id,
            size_id = size_data.size_id,
            quantity=size_data.quantity
        )
        session.add(sneaker_size)
    await session.commit()


async def delete_sneaker_sizes(session: AsyncSession, sneaker_sizes_delete: SneakerSizesDelete):
    stmt = delete(SneakerSizeAssociation).where(SneakerSizeAssociation.sneaker_id == sneaker_sizes_delete.sneaker_id).where(SneakerSizeAssociation.size_id.in_(sneaker_sizes_delete.size_ids))
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Размеры не найдены")


async def read_sneaker_sizes(session: AsyncSession, sneaker_id: int):
    stmt = (
        select(SneakerSizeAssociation)
        .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
    )
    result = await session.execute(stmt)
    sneaker_sizes = result.scalars().all()
    return sneaker_sizes
