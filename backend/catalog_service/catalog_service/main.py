from asyncio import create_task
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from catalog_service.catalog.config import settings
from catalog_service.catalog.kafka.kafka_handlers.sneaker_handler import handle_sneaker
from catalog_service.catalog.kafka.kafka_handlers.sneaker_sizes_handler import (
    handle_sneaker_sizes,
)
from catalog_service.catalog.models import db_helper
from catalog_service.add_middleware import add_middleware
from catalog_service import router as catalog_router
from kafka.consumer import start_consumer, close_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    sneaker_consumer, task_sneaker = await start_consumer(
        settings.kafka_config.sneaker_work_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.sneaker_group_id,
        handle_sneaker,
    )

    sneaker_sizes_consumer, task_sneaker_sizes = await start_consumer(
        settings.kafka_config.sneaker_sizes_work_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.sneaker_sizes_group_id,
        handle_sneaker_sizes,
    )

    yield
    task1 = create_task(close_consumer(sneaker_consumer, task_sneaker))
    task2 = create_task(close_consumer(sneaker_sizes_consumer, task_sneaker_sizes))
    await task1
    await task2

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    catalog_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
