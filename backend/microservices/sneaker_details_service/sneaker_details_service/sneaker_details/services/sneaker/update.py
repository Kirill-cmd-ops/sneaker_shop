from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import Sneaker


async def update_sneaker_service(
        session: AsyncSession,
        sneaker_id: int,
        sneaker_data: Dict[str, Any],
):
    async with session.begin():
        sneaker = await session.get(Sneaker, sneaker_id)
        for field, value in sneaker_data.items():
            setattr(sneaker, field, value)

        session.add(sneaker)
