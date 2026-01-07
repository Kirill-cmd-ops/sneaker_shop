from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from auth_service.auth.config import settings
from auth_service.auth.models import db_helper
from auth_service.add_middleware import add_middleware
from auth_service import router as auth_router

from kafka.producer import start_producer, close_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    producer = await start_producer(
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers
    )
    app.state.kafka_producer = producer
    yield
    # shutdown
    await close_producer(producer=producer)
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app=app)

app.include_router(
    auth_router,
)

# TODO: удалить, он лишний, мы все равно запускаем через docker compose
if __name__ == "__main__":
    uvicorn.run(
        app="auth_service.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
