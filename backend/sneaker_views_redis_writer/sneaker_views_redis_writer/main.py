from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from kafka.consumer import start_consumer, close_consumer
from sneaker_views_redis_writer.redis_writer.config import settings
from sneaker_views_redis_writer.add_middleware import add_middleware
from sneaker_views_redis_writer.redis_writer.kafka_handler.sneaker_views_redis_handler import (
    handle_sneaker_view_to_redis,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    sneaker_views_consumer, sneaker_views_task = await start_consumer(
        settings.kafka_config.sneaker_viewed_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.sneaker_views_redis_group,
        handle_sneaker_view_to_redis,
    )
    yield
    await close_consumer(sneaker_views_consumer, sneaker_views_task)


app = FastAPI(lifespan=lifespan)


add_middleware(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
