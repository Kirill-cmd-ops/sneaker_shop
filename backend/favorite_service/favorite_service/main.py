from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from favorite_service.favorite.config import settings
from favorite_service.favorite.kafka.kafka_handlers.favorite_handler import handle_favorite
from favorite_service.favorite.models import db_helper
from favorite_service.add_middleware import add_middleware
from favorite_service import router as favorite_router

from kafka.consumer import start_consumer, close_consumer



@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    favorite_consumer, task_favorite = await start_consumer(
        settings.kafka_config.registered_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.favorite_group_id,
        handle_favorite,
    )
    yield
    # shutdown
    await close_consumer(favorite_consumer, task_favorite)
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    favorite_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
