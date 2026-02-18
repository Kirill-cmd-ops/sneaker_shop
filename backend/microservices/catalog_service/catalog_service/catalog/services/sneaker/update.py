from typing import Dict, Any

from sqlalchemy.exc import IntegrityError

from microservices.catalog_service.catalog_service.catalog.models import Sneaker, db_helper


async def update_sneaker_service(
        sneaker_id: int,
        sneaker_data: Dict[str, Any],
) -> None:
    try:
        async with db_helper.session_context() as session:
            async with session.begin():
                sneaker = await session.get(Sneaker, sneaker_id)
                for field, value in sneaker_data.items():
                    setattr(sneaker, field, value)

                session.add(sneaker)
    except IntegrityError:
        return
