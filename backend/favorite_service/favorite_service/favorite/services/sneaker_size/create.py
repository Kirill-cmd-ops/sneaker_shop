from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import SneakerSizeAssociation
from favorite_service.favorite.schemas import SneakerSizesCreate


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