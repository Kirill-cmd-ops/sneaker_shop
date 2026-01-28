from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.kafka.consumer import start_consumer, close_consumer
from microservices.sneaker_views_clickhouse_writer.sneaker_views_clickhouse_writer.clickhouse_writer.config import \
    settings
from microservices.sneaker_views_clickhouse_writer.sneaker_views_clickhouse_writer.add_middleware import add_middleware
from microservices.sneaker_views_clickhouse_writer.sneaker_views_clickhouse_writer.clickhouse_writer.kafka.handlers.sneaker_views import (
    handle_sneaker_viewed_event,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    sneaker_views_consumer, sneaker_views_task = await start_consumer(
        topic=settings.kafka_config.sneaker_viewed_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.sneaker_views_clickhouse_group,
        handler=handle_sneaker_viewed_event,
    )
    yield
    await close_consumer(
        consumer=sneaker_views_consumer,
        task=sneaker_views_task,
    )


app = FastAPI(lifespan=lifespan)

add_middleware(app=app)
