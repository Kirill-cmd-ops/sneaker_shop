import asyncio
import contextlib
import json
from typing import Callable, Awaitable, Tuple

from aiokafka import AIOKafkaConsumer


async def start_consumer(
    topic: str,
    bootstrap_servers: str,
    group_id: str,
    handler: Callable[[str | None, dict], Awaitable[None]],
) -> Tuple[AIOKafkaConsumer, asyncio.Task]:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    await consumer.start()
    task = asyncio.create_task(_consume_loop(consumer, handler))
    return consumer, task


async def close_consumer(consumer: AIOKafkaConsumer, task: asyncio.Task) -> None:
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task
    await consumer.stop()


async def _consume_loop(consumer: AIOKafkaConsumer, handler):
    try:
        async for msg in consumer:
            await handler(msg.key, msg.value)
    except asyncio.CancelledError:
        pass
