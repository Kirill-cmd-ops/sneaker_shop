import functools

import redis.asyncio as aioredis
from fastapi import HTTPException
from starlette.requests import Request



def check_role_permissions(permission: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            redis_client: aioredis.Redis = kwargs.get("redis_client")

            user_role = request.headers.get("X-User-Role")
            if not user_role:
                raise HTTPException(status_code=401, detail="Не указан X-User-Role")

            key = f"role:{user_role}"
            has_permission = await redis_client.sismember(key, permission)

            if not has_permission:
                raise HTTPException(status_code=403, detail="У пользователя нет доступа")

            return await func(*args, **kwargs)
        return wrapper
    return decorator
