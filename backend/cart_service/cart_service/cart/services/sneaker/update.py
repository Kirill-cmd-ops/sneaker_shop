from cart_service.cart.models import Sneaker, db_helper
from cart_service.cart.schemas import SneakerUpdate


async def update_sneaker_service(
    sneaker_id: int,
    sneaker_update: SneakerUpdate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker = await session.get(Sneaker, sneaker_id)
            update_data = sneaker_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(sneaker, field, value)

            session.add(sneaker)
