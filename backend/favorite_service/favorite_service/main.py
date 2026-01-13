import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from favorite_service.favorite.config import settings
from favorite_service.favorite.kafka.handlers.brands import handle_brand_event
from favorite_service.favorite.kafka.handlers.favorites import (
    handle_favorite_event,
)
from favorite_service.favorite.kafka.handlers.sizes import handle_size_event
from favorite_service.favorite.kafka.handlers.sneakers import (
    handle_sneaker_event,
)
from favorite_service.favorite.kafka.handlers.sneaker_sizes import (
    handle_sneaker_sizes_event,
)
from favorite_service.favorite.models import db_helper
from favorite_service.add_middleware import add_middleware
from favorite_service import router as favorite_router

from kafka.consumer import start_consumer, close_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    sneaker_consumer, task_sneaker = await start_consumer(
        topic=settings.kafka_config.sneaker_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.sneaker_group_id,
        handler=handle_sneaker_event,
    )

    brand_consumer, task_brand = await start_consumer(
        topic=settings.kafka_config.brand_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.brand_group_id,
        handler=handle_brand_event,
    )

    size_consumer, task_size = await start_consumer(
        topic=settings.kafka_config.size_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.size_group_id,
        handler=handle_size_event,
    )

    sneaker_sizes_consumer, task_sneaker_sizes = await start_consumer(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.sneaker_sizes_group_id,
        handler=handle_sneaker_sizes_event,
    )

    favorite_consumer, task_favorite = await start_consumer(
        topic=settings.kafka_config.registered_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.favorite_group_id,
        handler=handle_favorite_event,
    )
    yield
    task1 = asyncio.create_task(
        close_consumer(
            consumer=sneaker_consumer,
            task=task_sneaker,
        )
    )
    task2 = asyncio.create_task(
        close_consumer(
            consumer=brand_consumer,
            task=task_brand,
        )
    )
    task3 = asyncio.create_task(
        close_consumer(
            consumer=size_consumer,
            task=task_size,
        )
    )
    task4 = asyncio.create_task(
        close_consumer(
            consumer=sneaker_sizes_consumer,
            task=task_sneaker_sizes,
        )
    )
    task5 = asyncio.create_task(
        close_consumer(
            consumer=favorite_consumer,
            task=task_favorite,
        )
    )

    await asyncio.gather(task1, task2, task3, task4, task5)

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app=app)

app.include_router(
    favorite_router,
)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
