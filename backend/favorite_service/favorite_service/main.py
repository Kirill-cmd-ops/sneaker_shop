from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from favorite_service.favorite.config import settings
from favorite_service.favorite.models import db_helper
from backend.add_middleware import add_middleware
from favorite_service import router as favorite_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
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