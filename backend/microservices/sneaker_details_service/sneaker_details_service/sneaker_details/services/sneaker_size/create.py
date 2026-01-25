from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import SneakerSizeAssociation
from sneaker_details_service.sneaker_details.schemas import SneakerSizesCreate


async def add_sizes_to_sneaker_service(
    session: AsyncSession,
    sneaker_id: int,
    sneaker_sizes_create: SneakerSizesCreate,
):
    sneaker_sizes = [
        {
            "sneaker_id": sneaker_id,
            "size_id": size_data.size_id,
            "quantity": size_data.quantity,
        }
        for size_data in sneaker_sizes_create.sizes
    ]

    async with session.begin():
        await session.execute(insert(SneakerSizeAssociation).values(sneaker_sizes))
