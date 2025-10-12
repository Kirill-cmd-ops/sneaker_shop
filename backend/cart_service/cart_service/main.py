from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.add_middleware import add_middleware
from cart_service import router as cart_router

from kafka.consumer import start_consumer, close_consumer

from cart_service.cart.kafka.kafka_handlers.cart_handler import handle_cart
from kafka.producer import start_producer, close_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    cart_producer = start_producer(
        settings.kafka_config.kafka_bootstrap_servers,
    )
    app.state.kafka_producer = cart_producer

    cart_consumer, task_cart = await start_consumer(
        settings.kafka_config.registered_topic,
        settings.kafka_config.kafka_bootstrap_servers,
        settings.kafka_config.cart_group_id,
        handle_cart,
    )
    yield
    # shutdown
    await close_producer(cart_producer)
    await close_consumer(cart_consumer, task_cart)
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
