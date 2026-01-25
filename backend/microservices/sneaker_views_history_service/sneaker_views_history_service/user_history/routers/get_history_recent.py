from asyncio import create_task

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import redis.asyncio as aioredis

from redis_client.redis_connection.factory import get_redis_factory
from sneaker_views_history_service.user_history.config import settings
from sneaker_views_history_service.user_history.dependencies.user_id import (
    get_current_user_id,
)
from sneaker_views_history_service.user_history.models.db_helper import db_helper
from sneaker_views_history_service.user_history.services.sneaker_view_history.create import (
    create_sneaker_view_history_service,
)
from sneaker_views_history_service.user_history.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)
from sneaker_views_history_service.user_history.services.sneaker_view_history.orchestrators import (
    get_user_sneaker_view_recent_history_orchestrator,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root, settings.api.v1.prefix, settings.api.v1.recent
    ),
    tags=["Sneakers Views"],
)


@router.get(
    "/",
    # dependencies=(Depends(check_role_permissions("favorite.view")),),
)
async def get_user_sneaker_view_recent_history(
    # request: Request,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(db_helper.session_getter),
    redis_client: aioredis.Redis = Depends(
        get_redis_factory(
            password=settings.redis_config.redis_password,
            host=settings.redis_config.redis_host,
            port=settings.redis_config.redis_port,
            db=settings.redis_config.redis_db,
        )
    ),
):
    # redis_client = request.state.redis_client

    return await get_user_sneaker_view_recent_history_orchestrator(
        user_id=user_id,
        session=session,
        redis_client=redis_client,
    )
