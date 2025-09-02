from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from kafka.producer import start_producer, close_producer
from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.models import db_helper
from sneaker_details_service.add_middleware import add_middleware
from sneaker_details_service import router as sneaker_details_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = await start_producer(settings.kafka_config.kafka_bootstrap_servers)
    app.state.kafka_producer = producer
    # startup
    yield
    # shutdown
    await close_producer(producer)
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    sneaker_details_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
