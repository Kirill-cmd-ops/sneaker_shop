from asyncio import create_task

from starlette.requests import Request


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import redis.asyncio as aioredis

from redis_client.redis_connection.factory import get_redis_factory
from user_history_service.user_history.config import settings
from user_history_service.user_history.dependencies.check_permissions import (
    check_role_permissions,
)
from user_history_service.user_history.dependencies.get_current_user import (
    get_user_by_header,
)
from user_history_service.user_history.models import SneakerViewsHistory
from user_history_service.user_history.models.db_helper import db_helper
from user_history_service.user_history.services.get_views_clickhouse import (
    get_sneaker_views_clickhouse,
)
from user_history_service.user_history.services.write_sneaker_views_redis import (
    sneaker_view_to_redis,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.recent_sneakers_views
    ),
    tags=["Sneakers Views"],
)


redis_factory = get_redis_factory(
    settings.redis_config.redis_password,
    settings.redis_config.redis_host,
    settings.redis_config.redis_port,
    settings.redis_config.redis_db,
)


@router.post("/get_history_clickhouse/")
async def call_get_sneaker_views_clickhouse(
    session: Session = Depends(db_helper.session_getter),
    user_id: int = Depends(get_user_by_header),
):
    record = await get_sneaker_views_clickhouse(session, user_id)
    return record



