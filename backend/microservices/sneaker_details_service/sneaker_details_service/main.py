from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.kafka.producer import start_producer, close_producer
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper
from microservices.sneaker_details_service.sneaker_details_service.add_middleware import add_middleware
from microservices.sneaker_details_service.sneaker_details_service import router as sneaker_details_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = await start_producer(
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
    )
    app.state.kafka_producer = producer
    # startup
    yield
    # shutdown
    await close_producer(producer=producer)
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

add_middleware(app=app)

app.include_router(
    sneaker_details_router,
)
