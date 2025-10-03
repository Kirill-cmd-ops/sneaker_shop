from asyncio import create_task

from starlette.requests import Request


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import redis.asyncio as aioredis

from redis_client.redis_connection.factory import get_redis_factory
from sneaker_views_history_service.user_history.config import settings
from sneaker_views_history_service.user_history.dependencies.check_permissions import (
    check_role_permissions,
)
from sneaker_views_history_service.user_history.dependencies.get_current_user import (
    get_user_by_header,
)
from sneaker_views_history_service.user_history.models import SneakerViewsHistory
from sneaker_views_history_service.user_history.models.db_helper import db_helper
from sneaker_views_history_service.user_history.services.get_sneaker_views_clickhouse import (
    clickhouse_select,
)
from sneaker_views_history_service.user_history.services.add_sneaker_views_redis import (
    redis_insert,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.recent_sneakers_views
    ),
    tags=["Sneakers Views"],
)


@router.post("/get_history_clickhouse/")
async def call_get_sneaker_views_clickhouse(
    session: Session = Depends(db_helper.session_getter),
    user_id: int = Depends(get_user_by_header),
):
    record = await clickhouse_select(session, user_id)
    return record


@router.post(
    "/get_history/",
    # dependencies=(Depends(check_role_permissions("favorite.view")),),
)
async def get_sneaker_views(
    # request: Request,
    user_id: int,
    session: Session = Depends(db_helper.session_getter),
    redis_client: aioredis.Redis = Depends(
        get_redis_factory(
            settings.redis_config.redis_password,
            settings.redis_config.redis_host,
            settings.redis_config.redis_port,
            settings.redis_config.redis_db,
        )
    ),
):
    # redis_client = request.state.redis_client

    records = await redis_client.zrange(f"views:{user_id}", 0, -1)
    if not records:
        records = await clickhouse_select(session, user_id, 30)

        task = create_task(
            redis_insert(
                records=records,
            )
        )
    return records
