import redis.asyncio as aioredis
from fastapi import HTTPException, Depends
from starlette.requests import Request

from auth_service.auth.config import settings
from auth_service.auth.dependencies.get_current_user_role import get_user_role_by_header
from redis_client.redis_connection.factory import get_redis_factory



def check_role_permissions(
    permission: str,
):

    async def checker(
        request: Request,
        redis_client: aioredis.Redis = Depends(
            get_redis_factory(
                settings.redis_config.redis_password,
                settings.redis_config.redis_host,
                settings.redis_config.redis_port,
                settings.redis_config.redis_db,
            )
        ),
        user_role: str = Depends(get_user_role_by_header),
    ):
        request.state.redis_client = redis_client
        request.state.user_role = user_role

        if not user_role:
            raise HTTPException(status_code=401, detail="Не указан X-User-Role")

        key = f"role:{user_role}"
        has_permission = await redis_client.sismember(key, permission)

        if not has_permission:
            raise HTTPException(status_code=403, detail="У пользователя нет доступа")
    return checker
