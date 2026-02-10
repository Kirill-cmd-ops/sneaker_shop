from typing import Dict, Any

from sqlalchemy.exc import IntegrityError

from microservices.catalog_service.catalog_service.catalog.models import Sneaker, SneakerSizeAssociation, db_helper


async def create_sneaker_service(
        sneaker_data: Dict[str, Any],
        size_ids: list[Dict[str, Any]],
):
    try:
        async with db_helper.session_context() as session:
            async with session.begin():
                sneaker = Sneaker(**sneaker_data)
                session.add(sneaker)
                await session.flush()

                if size_ids:
                    for size in size_ids:
                        sneaker_sizes = SneakerSizeAssociation(
                            sneaker_id=sneaker.id,
                            size_id=size["size_id"],
                            quantity=size["quantity"],
                        )
                        session.add(sneaker_sizes)
    except IntegrityError:
        return
