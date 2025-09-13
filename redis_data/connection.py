import redis.asyncio as aioredis

from auth_service.auth.config import settings

async def get_redis():
    redis_client = aioredis.Redis(
        host="redis",
        port=6379,
        db=0,
        password=settings.redis_config.redis_password,
        protocol=3,
        decode_responses=True,
    )
    try:
        yield redis_client
    finally:
        await redis_client.aclose()

