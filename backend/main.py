from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from backend.middlewares import add_middleware
from backend.auth.config import settings

from backend.api import router as api_router
from backend.auth.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.mount("/uploads/sneakers", StaticFiles(directory="backend/static/uploads/sneakers"), name="sneakers")
app.mount("/uploads/brands", StaticFiles(directory="backend/static/uploads/brands"), name="brands")


add_middleware(app)

app.include_router(
    api_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
