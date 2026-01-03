from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import Sneaker, SneakerSizeAssociation
from cart_service.cart.schemas import SneakerCreate


async def create_sneaker(
    session: AsyncSession,
    sneaker_create: SneakerCreate,
):
    sneaker = Sneaker(**sneaker_create.dict(exclude="size_ids"))
    session.add(sneaker)
    await session.flush()

    for size in sneaker_create.size_ids:
        sneaker_sizes = SneakerSizeAssociation(
            sneaker_id=sneaker.id, size_id=size.size_id, quantity=size.quantity
        )
        session.add(sneaker_sizes)

    await session.commit()
