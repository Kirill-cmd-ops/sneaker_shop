from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import SneakerSizeAssociation
from favorite_service.favorite.schemas import SneakerSizeUpdate


async def update_sneaker_size_quantity_service(
    session: AsyncSession, sneaker_id: int, sneaker_size_update: SneakerSizeUpdate
):
    sneaker_size = await session.scalar(
        select(SneakerSizeAssociation)
        .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
        .where(SneakerSizeAssociation.size_id == sneaker_size_update.size.size_id)
    )

    sneaker_size.quantity = sneaker_size_update.size.quantity

    session.add(sneaker_size)
    await session.commit()
