from contextlib import asynccontextmanager

from fastapi import FastAPI

from microservices.sneaker_views_history_service.sneaker_views_history_service.add_middleware import add_middleware
from microservices.sneaker_views_history_service.sneaker_views_history_service import router as user_history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

add_middleware(app=app)

app.include_router(
    user_history_router,
)
