import redis.asyncio as aioredis
from fastapi import HTTPException, Depends
from starlette.requests import Request

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.dependencies.get_current_user_role import (
    get_user_role_by_header,
)
from redis_client.redis_connection.factory import get_redis_factory


def check_role_permissions(
    permission: str,
):

    async def checker(
        request: Request,
        redis_client: aioredis.Redis = Depends(
            get_redis_factory(
                password=settings.redis_config.redis_password,
                host=settings.redis_config.redis_host,
                port=settings.redis_config.redis_port,
                db=settings.redis_config.redis_db,
            )
        ),
        user_role: str = Depends(get_user_role_by_header),
    ):
        request.state.redis_client = redis_client
        request.state.user_role = user_role

        if not user_role:
            raise HTTPException(status_code=401, detail="Не указан X-User-Role")

        key = f"user_role:{user_role}"
        has_permission = await redis_client.sismember(key, permission)

        if not has_permission:
            raise HTTPException(status_code=403, detail="У пользователя нет доступа")

    return checker
