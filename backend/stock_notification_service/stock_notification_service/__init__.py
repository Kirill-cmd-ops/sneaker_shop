from fastapi import APIRouter

from stock_notification_service.stock_notification.routers.stock_notification import router as stock_notification_router

router = APIRouter()

router.include_router(stock_notification_router)