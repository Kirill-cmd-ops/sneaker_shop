from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from catalog_service.catalog.config import settings
from catalog_service.catalog.models import db_helper
from catalog_service.add_middleware import add_middleware
from catalog_service import router as catalog_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    catalog_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )