from sqlalchemy import select

from catalog_service.catalog.models import SneakerSizeAssociation, db_helper
from catalog_service.catalog.schemas import SneakerSizeUpdate


async def update_sneaker_size_quantity_service(
    sneaker_id: int,
    sneaker_size_update: SneakerSizeUpdate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker_size = await session.scalar(
                select(SneakerSizeAssociation)
                .where(SneakerSizeAssociation.sneaker_id == sneaker_id)
                .where(
                    SneakerSizeAssociation.size_id == sneaker_size_update.size.size_id
                )
            )

            sneaker_size.quantity = sneaker_size_update.size.quantity

            session.add(sneaker_size)
