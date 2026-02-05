from typing import Dict, Any

from microservices.cart_service.cart_service.cart.models import Sneaker, db_helper


async def update_sneaker_service(
        sneaker_id: int,
        sneaker_data: Dict[str, Any],
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker = await session.get(Sneaker, sneaker_id)
            for field, value in sneaker_data.items():
                setattr(sneaker, field, value)

            session.add(sneaker)
