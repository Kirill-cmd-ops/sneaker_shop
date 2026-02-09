from typing import Dict, Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from microservices.favorite_service.favorite_service.favorite.models import SneakerSizeAssociation, db_helper


async def add_sizes_to_sneaker_service(
        sneaker_id: int,
        size_list: list[Dict[str, Any]],
):
    try:
        async with db_helper.session_context() as session:
            async with session.begin():
                sneaker_sizes = [
                    {
                        "sneaker_id": sneaker_id,
                        "size_id": size_data["size_id"],
                        "quantity": size_data["quantity"],
                    }
                    for size_data in size_list
                ]

                await session.execute(insert(SneakerSizeAssociation).values(sneaker_sizes))
    except IntegrityError:
        return
