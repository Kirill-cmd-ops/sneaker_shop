import time

from infrastructure.redis_client.redis_connection.factory import get_redis_factory
from microservices.sneaker_views_history_service.sneaker_views_history_service.user_history.config import settings

redis_factory = get_redis_factory(
    password=settings.redis_config.redis_password,
    host=settings.redis_config.redis_host,
    port=settings.redis_config.redis_port,
    db=settings.redis_config.redis_db,
)


async def create_sneaker_view_history_service(records):
    async for redis_client in redis_factory():
        user_data = {}

        for record in records:
            user_id = record.user_id
            sneaker_id = record.sneaker_id

            if user_id not in user_data:
                user_data[user_id] = []

            user_data[user_id].append(sneaker_id)

        async with redis_client.pipeline(transaction=True) as pipe:
            for user_id, sneaker_ids in user_data.items():
                user_views_key = f"views:{user_id}"
                score = int(time.time())

                value_payload = {
                    f"sneaker_{sneaker_id}": score for sneaker_id in sneaker_ids
                }
                await pipe.zadd(user_views_key, value_payload)
                await pipe.expire(user_views_key, 2592000)
                await pipe.zremrangebyrank(user_views_key, 0, -31)
            await pipe.execute()
