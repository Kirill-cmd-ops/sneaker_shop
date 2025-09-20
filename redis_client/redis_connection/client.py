import redis.asyncio as aioredis


async def get_redis(
    password: str,
    host: str = "redis",
    port: int = 6379,
    db: int = 0,
):
    return aioredis.Redis(
        host=host,
        port=port,
        db=db,
        password=password,
        protocol=3,
        decode_responses=True,
    )
