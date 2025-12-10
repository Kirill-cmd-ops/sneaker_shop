from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.schemas import (
    SneakerSizesCreate,
    SneakerSizeUpdate,
)

from sneaker_details_service.sneaker_details.models import SneakerSizeAssociation


async def create_sneaker_sizes(
    session: AsyncSession, sneaker_id: int, sneaker_sizes_create: SneakerSizesCreate
):
    for size_data in sneaker_sizes_create.sizes:
        sneaker_size = SneakerSizeAssociation(
            sneaker_id=sneaker_id,
            size_id=size_data.size_id,
            quantity=size_data.quantity,
        )
        session.add(sneaker_size)
    await session.commit()


async def update_sneaker_sizes(
    session: AsyncSession, sneaker_id: int, sneaker_size_update: SneakerSizeUpdate
):
    stmt = (
        select(SneakerSizeAssociation)
        .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
        .where(SneakerSizeAssociation.size_id == sneaker_size_update.size.size_id)
    )
    result = await session.execute(stmt)
    sneaker_size = result.scalar_one()

    sneaker_size.quantity = sneaker_size_update.size.quantity

    session.add(sneaker_size)
    await session.commit()
