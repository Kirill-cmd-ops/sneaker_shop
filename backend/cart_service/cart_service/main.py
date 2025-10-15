import asyncio
from asyncio import create_task
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from cart_service.cart.config import settings
from cart_service.cart.kafka.kafka_handlers.sneaker_handler import handle_sneaker
from cart_service.cart.kafka.kafka_handlers.sneaker_sizes_handler import handle_sneaker_sizes
from cart_service.cart.models import db_helper
from cart_service.add_middleware import add_middleware
from cart_service import router as cart_router

from kafka.consumer import start_consumer, close_consumer

from cart_service.cart.kafka.kafka_handlers.cart_handler import handle_cart


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
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

    cart_consumer, task_cart = await start_consumer(
        settings.kafka_config.registered_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.cart_group_id,
        handle_cart,
    )
    yield
    task1 = create_task(close_consumer(sneaker_consumer, task_sneaker))
    task2 = create_task(close_consumer(sneaker_sizes_consumer, task_sneaker_sizes))
    task3 = create_task(close_consumer(cart_consumer, task_cart))

    await asyncio.gather(task1, task2, task3)

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    cart_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
