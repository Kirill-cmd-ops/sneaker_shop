from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.catalog.models import Sneaker, SneakerSizeAssociation, db_helper
from catalog_service.catalog.schemas import SneakerCreate


async def create_sneaker_service(
    sneaker_create: SneakerCreate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            sneaker = Sneaker(**sneaker_create.dict(exclude="size_ids"))
            session.add(sneaker)
            await session.flush()

            if sneaker_create.size_ids:
                for size in sneaker_create.size_ids:
                    sneaker_sizes = SneakerSizeAssociation(
                        sneaker_id=sneaker.id,
                        size_id=size.size_id,
                        quantity=size.quantity,
                    )
                    session.add(sneaker_sizes)
