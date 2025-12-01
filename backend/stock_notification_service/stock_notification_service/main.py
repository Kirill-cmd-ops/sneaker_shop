from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from stock_notification_service.stock_notification.config import settings

from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.add_middleware import add_middleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield

    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


add_middleware(app)

# TODO: удалить, он лишний, мы все равно запускаем через docker compose
if __name__ == "__main__":
    uvicorn.run(
        "stock_notification_service.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
