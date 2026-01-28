from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import Sneaker
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import SneakerUpdate


async def update_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
        sneaker_update: SneakerUpdate,
):
    async with session.begin():
        sneaker = await session.get(Sneaker, sneaker_id)
        update_data = sneaker_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(sneaker, field, value)

        session.add(sneaker)
