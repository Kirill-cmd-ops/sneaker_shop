import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from favorite_service.favorite.config import settings
from favorite_service.favorite.kafka.kafka_handlers.brand_handler import handle_brand
from favorite_service.favorite.kafka.kafka_handlers.favorite_handler import handle_favorite
from favorite_service.favorite.kafka.kafka_handlers.size_handler import handle_size
from favorite_service.favorite.kafka.kafka_handlers.sneaker_handler import handle_sneaker
from favorite_service.favorite.kafka.kafka_handlers.sneaker_sizes_handler import handle_sneaker_sizes
from favorite_service.favorite.models import db_helper
from favorite_service.add_middleware import add_middleware
from favorite_service import router as favorite_router

from kafka.consumer import start_consumer, close_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    sneaker_consumer, task_sneaker = await start_consumer(
        settings.kafka_config.sneaker_work_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.sneaker_group_id,
        handle_sneaker,
    )

    brand_consumer, task_brand = await start_consumer(
        settings.kafka_config.brand_work_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.brand_group_id,
        handle_brand,
    )

    size_consumer, task_size = await start_consumer(
        settings.kafka_config.size_work_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.size_group_id,
        handle_size,
    )

    sneaker_sizes_consumer, task_sneaker_sizes = await start_consumer(
        settings.kafka_config.sneaker_sizes_work_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.sneaker_sizes_group_id,
        handle_sneaker_sizes,
    )

    favorite_consumer, task_favorite = await start_consumer(
        settings.kafka_config.registered_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.favorite_group_id,
        handle_favorite,
    )
    yield
    task1 = asyncio.create_task(close_consumer(sneaker_consumer, task_sneaker))
    task2 = asyncio.create_task(close_consumer(brand_consumer, task_brand))
    task3 = asyncio.create_task(close_consumer(size_consumer, task_size))
    task4 = asyncio.create_task(close_consumer(sneaker_sizes_consumer, task_sneaker_sizes))
    task5 = asyncio.create_task(close_consumer(favorite_consumer, task_favorite))

    await asyncio.gather(task1, task2, task3, task4, task5)

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    favorite_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
