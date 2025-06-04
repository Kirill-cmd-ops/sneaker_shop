from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from cart_service.cart.config import settings
from cart_service.cart.models import db_helper
from cart_service.add_middleware import add_middleware
from cart_service import router as cart_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
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