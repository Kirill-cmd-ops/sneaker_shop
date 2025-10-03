from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from user_history_service.user_history.config import settings
from user_history_service.add_middleware import add_middleware
from user_history_service import router as user_history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)


add_middleware(app)

app.include_router(
    user_history_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
