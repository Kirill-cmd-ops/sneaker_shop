import asyncio
import contextlib
from typing import Callable, Awaitable

from aiokafka import AIOKafkaConsumer


async def start_consumer(
    consumer: AIOKafkaConsumer, handler: Callable[[str | None, dict], Awaitable[None]]
) -> asyncio.Task:
    await consumer.start()
    task = asyncio.create_task(_consume_loop(consumer, handler))
    return task


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
        return
