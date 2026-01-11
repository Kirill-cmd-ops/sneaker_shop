import redis.asyncio as aioredis
from fastapi import HTTPException, Depends
from starlette.requests import Request

from cart_service.cart.config import settings
from cart_service.cart.dependencies.user_role import get_current_user_role
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
        user_role: str = Depends(get_current_user_role),
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
