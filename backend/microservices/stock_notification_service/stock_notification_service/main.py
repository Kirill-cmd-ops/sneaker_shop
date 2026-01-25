import asyncio
from asyncio import create_task
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from kafka.consumer import start_consumer, close_consumer
from stock_notification_service.stock_notification.config import settings
from stock_notification_service.stock_notification.kafka.handlers.brands import (
    handle_brand_event,
)
from stock_notification_service.stock_notification.kafka.handlers.sizes import (
    handle_size_event,
)
from stock_notification_service.stock_notification.kafka.handlers.sneaker_active import (
    handle_sneaker_active_event,
)
from stock_notification_service.stock_notification.kafka.handlers.sneakers import (
    handle_sneaker_event,
)
from stock_notification_service.stock_notification.kafka.handlers.sneaker_sizes import (
    handle_sneaker_sizes_event,
)
from stock_notification_service.stock_notification.kafka.handlers.users import (
    handle_user_event,
)
from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.add_middleware import add_middleware

from stock_notification_service import router as stock_notification_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    sneaker_consumer, task_sneaker = await start_consumer(
        topic=settings.kafka_config.sneaker_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.sneaker_group_id,
        handler=handle_sneaker_event,
    )

    sneaker_active_consumer, task_sneaker_active = await start_consumer(
        topic=settings.kafka_config.sneaker_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.sneaker_active_group_id,
        handler=handle_sneaker_active_event,
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

    user_consumer, task_user = await start_consumer(
        topic=settings.kafka_config.user_work_topic,
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        group_id=settings.kafka_config.user_group_id,
        handler=handle_user_event,
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
            consumer=sneaker_active_consumer,
            task=task_sneaker_active,
        )
    )
    task3 = create_task(
        close_consumer(
            consumer=brand_consumer,
            task=task_brand,
        )
    )
    task4 = create_task(
        close_consumer(
            consumer=size_consumer,
            task=task_size,
        )
    )
    task5 = create_task(
        close_consumer(
            consumer=sneaker_sizes_consumer,
            task=task_sneaker_sizes,
        )
    )
    task6 = create_task(
        close_consumer(
            consumer=user_consumer,
            task=task_user,
        )
    )

    await asyncio.gather(task1, task2, task3, task4, task5, task6)

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app=app)

app.include_router(stock_notification_router)

# TODO: удалить, он лишний, мы все равно запускаем через docker compose
if __name__ == "__main__":
    uvicorn.run(
        app="stock_notification_service.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
