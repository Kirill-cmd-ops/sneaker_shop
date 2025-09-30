import time

import redis.asyncio as aioredis

from user_history_service.user_history.models import SneakerViewsHistory


async def sneaker_view_to_redis(
    records,
    redis_client: aioredis.Redis,
):
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
