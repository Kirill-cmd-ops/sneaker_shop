import time

from redis_client.redis_connection.client import get_redis

from sneaker_views_redis_writer.sneaker_views.config import settings


async def handle_sneaker_view_to_redis(
    key: str | None,
    value: dict,
):
    redis_client = await get_redis(
        settings.redis_config.redis_password,
        settings.redis_config.redis_host,
        settings.redis_config.redis_port,
        settings.redis_config.redis_db,
    )

    user_id = value.get("user_id")
    sneaker_id = value.get("sneaker_id")

    score = int(time.time())

    value_payload = {
        f"sneaker_{sneaker_id}": score,
    }

    user_views_key = f"views:{user_id}"

    async with redis_client.pipeline() as pipe:
        await pipe.zadd(user_views_key, value_payload)
        await pipe.expire(user_views_key, 2592000)
        await pipe.zremrangebyrank(user_views_key, 0, -51)
        await pipe.execute()
