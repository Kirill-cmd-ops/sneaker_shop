from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.auth_service.auth_service.auth.config import settings
from backend.auth_service.auth_service.auth.models import db_helper
from backend.middlewares import add_middleware
from backend.auth_service.auth_service import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    auth_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )