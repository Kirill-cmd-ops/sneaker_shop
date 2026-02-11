from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.kafka.producer import start_producer, close_producer
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.domain.exceptions import \
    RecordAlreadyExists, SneakerNotFound, SneakerAlreadyExists, SneakerAssociationAlreadyExists, \
    SneakerSizeAlreadyExists, SneakerSizeNotFound
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper
from microservices.sneaker_details_service.sneaker_details_service.add_middleware import add_middleware
from microservices.sneaker_details_service.sneaker_details_service import router as sneaker_details_router
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.routers.exception_handlers import \
    record_already_exists_handler, sneaker_not_found_handler, sneaker_already_exists_handler, \
    sneaker_association_already_exists_handler, sneaker_size_already_exists_handler, sneaker_size_not_found_handler


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


app.add_exception_handler(RecordAlreadyExists, record_already_exists_handler)
app.add_exception_handler(SneakerNotFound, sneaker_not_found_handler)
app.add_exception_handler(SneakerAlreadyExists, sneaker_already_exists_handler)
app.add_exception_handler(SneakerAssociationAlreadyExists, sneaker_association_already_exists_handler)
app.add_exception_handler(SneakerSizeAlreadyExists, sneaker_size_already_exists_handler)
app.add_exception_handler(SneakerSizeNotFound, sneaker_size_not_found_handler)