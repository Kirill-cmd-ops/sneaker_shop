from contextlib import asynccontextmanager

from fastapi import FastAPI

from microservices.auth_service.auth_service.auth.domain.exceptions import RoleNotFound, UserNotFound, UserRoleAssociationAlreadyExists, \
    BlacklistAlreadyExists
from microservices.auth_service.auth_service.auth.routers.exception_handlers import role_not_found_handler, user_not_found_handler, \
    user_role_association_already_exists_handler, blacklist_already_exists_handler
from microservices.auth_service.auth_service.auth.config import settings
from microservices.auth_service.auth_service.auth.models import db_helper
from microservices.auth_service.auth_service.add_middleware import add_middleware
from microservices.auth_service.auth_service import router as auth_router

from infrastructure.kafka.producer import start_producer, close_producer


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

app.add_exception_handler(RoleNotFound, role_not_found_handler)
app.add_exception_handler(UserNotFound, user_not_found_handler)
app.add_exception_handler(UserRoleAssociationAlreadyExists, user_role_association_already_exists_handler)
app.add_exception_handler(BlacklistAlreadyExists, blacklist_already_exists_handler)
