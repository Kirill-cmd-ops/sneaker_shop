from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import \
    SneakerSizeNotFound
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import SneakerSizeAssociation


async def update_sneaker_size_quantity_service(
        session: AsyncSession,
        sneaker_id: int,
        size_id: int,
        quantity: int,
) -> SneakerSizeAssociation:
    async with session.begin():
        sneaker_size = await session.scalar(
            select(SneakerSizeAssociation)
            .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
            .where(SneakerSizeAssociation.size_id == size_id)
        )

        if not sneaker_size:
            raise SneakerSizeNotFound()

        sneaker_size.quantity = quantity

        session.add(sneaker_size)
    
    return sneaker_size
