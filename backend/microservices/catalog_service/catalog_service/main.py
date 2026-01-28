import asyncio
from asyncio import create_task
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from microservices.catalog_service.catalog_service.catalog.config import settings
from microservices.catalog_service.catalog_service.catalog.kafka.handlers.brands import handle_brand_event
from microservices.catalog_service.catalog_service.catalog.kafka.handlers.sizes import handle_size_event
from microservices.catalog_service.catalog_service.catalog.kafka.handlers.sneakers import handle_sneaker_event
from microservices.catalog_service.catalog_service.catalog.kafka.handlers.sneaker_sizes import (
    handle_sneaker_sizes_event,
)
from microservices.catalog_service.catalog_service.catalog.models import db_helper
from microservices.catalog_service.catalog_service.add_middleware import add_middleware
from microservices.catalog_service.catalog_service import router as catalog_router
from infrastructure.kafka.consumer import start_consumer, close_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
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

    await asyncio.gather(task1, task2, task3, task4)

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

add_middleware(app=app)

app.include_router(
    catalog_router,
)

# Раздача статических файлов (картинки кроссовок и брендов)
# Путь к статике в контейнере: /app/static
static_path = Path("/app/static")
if not static_path.exists():
    # Fallback для локальной разработки
    static_path = Path(__file__).parent.parent.parent.parent / "static"

if static_path.exists():
    uploads_path = static_path / "uploads"
    if uploads_path.exists():
        try:
            app.mount("/uploads", StaticFiles(directory=str(uploads_path)), name="static")
            print(f"✅ Статические файлы подключены из: {uploads_path}")
        except Exception as e:
            print(f"❌ Ошибка подключения статических файлов: {e}")
    else:
        print(f"⚠️  Папка uploads не найдена: {uploads_path}")
else:
    print(f"⚠️  Папка static не найдена: {static_path}")
