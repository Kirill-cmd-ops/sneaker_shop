from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import SneakerSizeAssociation
from sneaker_details_service.sneaker_details.schemas import SneakerSizesCreate


async def create_sneaker_sizes(
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

    await session.execute(insert(SneakerSizeAssociation).values(sneaker_sizes))

    await session.commit()
