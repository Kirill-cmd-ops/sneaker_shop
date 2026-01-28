from asyncio import create_task

import redis.asyncio as aioredis

from sqlalchemy.orm import Session

from microservices.sneaker_views_history_service.sneaker_views_history_service.user_history.services.sneaker_view_history.create import (
    create_sneaker_view_history_service,
)
from microservices.sneaker_views_history_service.sneaker_views_history_service.user_history.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)


async def get_user_sneaker_view_recent_history_orchestrator(
        user_id: int,
        session: Session,
        redis_client: aioredis.Redis,
):
    records = await redis_client.zrange(
        name=f"views:{user_id}",
        start=0,
        end=-1,
    )
    if not records:
        records = await get_user_sneaker_view_history_service(
            session=session,
            user_id=user_id,
            limit=30,
        )

        task = create_task(create_sneaker_view_history_service(records=records))
    return records
