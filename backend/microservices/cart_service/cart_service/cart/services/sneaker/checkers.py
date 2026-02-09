from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.domain.exceptions import SneakerNotFound
from microservices.cart_service.cart_service.cart.models import Sneaker


async def check_sneaker_exists_service(
        session: AsyncSession,
        sneaker_id: int,
):
    sneaker = await session.get(Sneaker, sneaker_id)
    if not sneaker:
        raise SneakerNotFound()
