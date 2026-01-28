import asyncio
from asyncio import create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI

from microservices.cart_service.cart_service.cart.config import settings
from microservices.cart_service.cart_service.cart.kafka.handlers.brands import handle_brand_event
from microservices.cart_service.cart_service.cart.kafka.handlers.sizes import handle_size_event
from microservices.cart_service.cart_service.cart.kafka.handlers.sneakers import handle_sneaker_event
from microservices.cart_service.cart_service.cart.kafka.handlers.sneaker_sizes import (
    handle_sneaker_sizes_event,
)
from microservices.cart_service.cart_service.cart.models import db_helper
from microservices.cart_service.cart_service.add_middleware import add_middleware
from microservices.cart_service.cart_service import router as cart_router

from infrastructure.kafka.consumer import start_consumer, close_consumer

from microservices.cart_service.cart_service.cart.kafka.handlers.carts import handle_cart_event


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

    cart_consumer, task_cart = await start_consumer(
        topic=settings.kafka_config.registered_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.cart_group_id,
        handler=handle_cart_event,
    )
    yield
    task1 = create_task(
        close_consumer(
            consumer=sneaker_consumer,
            task=task_sneaker,
        )
    )
    task2 = create_task(
        close_consumer(
            consumer=brand_consumer,
            task=task_brand,
        )
    )
    task3 = create_task(
        close_consumer(
            consumer=size_consumer,
            task=task_size,
        )
    )
    task4 = create_task(
        close_consumer(
            consumer=sneaker_sizes_consumer,
            task=task_sneaker_sizes,
        )
    )
    task5 = create_task(
        close_consumer(
            consumer=cart_consumer,
            task=task_cart,
        )
    )

    await asyncio.gather(task1, task2, task3, task4, task5)

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

add_middleware(app=app)

app.include_router(
    cart_router,
)
