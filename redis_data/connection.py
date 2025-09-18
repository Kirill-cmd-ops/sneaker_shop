import redis.asyncio as aioredis


def get_redis_factory(
    password: str,
    host: str = "redis",
    port: int = 6379,
    db: int = 0,
):
    async def get_redis():
        redis_client = aioredis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            protocol=3,
            decode_responses=True,
        )
        try:
            yield redis_client
        finally:
            await redis_client.aclose()

    return get_redis
