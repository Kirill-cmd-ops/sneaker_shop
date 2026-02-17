from sqlalchemy import select

from microservices.favorite_service.favorite_service.favorite.models import SneakerSizeAssociation, db_helper


async def update_sneaker_size_quantity_service(
        sneaker_id: int,
        size_id: int,
        quantity: int,
) -> None:
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker_size = await session.scalar(
                select(SneakerSizeAssociation)
                .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
                .where(
                    SneakerSizeAssociation.size_id == size_id
                )
            )

            sneaker_size.quantity = quantity

            session.add(sneaker_size)
