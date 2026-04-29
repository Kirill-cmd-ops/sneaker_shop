from asyncio import create_task
from datetime import datetime
from typing import Sequence

import redis.asyncio as aioredis

from sqlalchemy.orm import Session

from microservices.sneaker_views_history_service.sneaker_views_history_service.user_history.models import (
    SneakerViewsHistory,
)
from microservices.sneaker_views_history_service.sneaker_views_history_service.user_history.services.sneaker_view_history.create import (
    create_sneaker_view_history_service,
)
from microservices.sneaker_views_history_service.sneaker_views_history_service.user_history.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)


def history_rows_from_redis_zset(
        user_id: int,
        members_with_scores: list[tuple[bytes | str, float]],
) -> list[SneakerViewsHistory]:
    rows: list[SneakerViewsHistory] = []
    for member, score in members_with_scores:
        key = (
            member.decode()
            if isinstance(member, (bytes, bytearray))
            else str(member)
        )
        prefix = "sneaker_"
        if not key.startswith(prefix):
            continue
        sneaker_id = int(key[len(prefix):])
        ts = int(score)
        rows.append(
            SneakerViewsHistory(
                user_id=user_id,
                sneaker_id=sneaker_id,
                view_timestamp=datetime.utcfromtimestamp(ts),
                sign=1,
                version=ts,
            ),
        )
    return rows


async def get_user_sneaker_view_recent_history_orchestrator(
        user_id: int,
        session: Session,
        redis_client: aioredis.Redis,
) -> Sequence[SneakerViewsHistory]:
    members_with_scores = await redis_client.zrange(
        name=f"views:{user_id}",
        start=0,
        end=-1,
        desc=True,
        withscores=True,
    )
    if not members_with_scores:
        db_records = await get_user_sneaker_view_history_service(
            session=session,
            user_id=user_id,
            limit=30,
        )
        create_task(create_sneaker_view_history_service(records=db_records))
        return list(db_records)

    return history_rows_from_redis_zset(user_id, members_with_scores)
