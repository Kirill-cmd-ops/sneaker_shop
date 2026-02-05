from typing import Callable, Dict, Any

from microservices.favorite_service.favorite_service.favorite.models import db_helper


async def create_record_service(
        table_name: Callable,
        data: Dict[str, Any],
):
    async with db_helper.session_context() as session:
        async with session.begin():
            new_record = table_name(**data)
            session.add(new_record)
