from sqlalchemy.dialects.postgresql import insert

from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    SneakerSizeAssociation,
    db_helper,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas import \
    SneakerSizesCreate


async def add_sizes_to_sneaker_service(
        sneaker_id: int,
        sneaker_sizes_create: SneakerSizesCreate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker_sizes = [
                {
                    "sneaker_id": sneaker_id,
                    "size_id": size_data.size_id,
                    "quantity": size_data.quantity,
                }
                for size_data in sneaker_sizes_create.sizes
            ]

            await session.execute(insert(SneakerSizeAssociation).values(sneaker_sizes))
