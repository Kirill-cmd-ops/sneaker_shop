from fastapi import APIRouter

from stock_notification_service.stock_notification.routers.permanent_subscription import (
    router as permanent_subscriptions_router,
)
from stock_notification_service.stock_notification.routers.one_time_subscription import (
    router as one_time_subscriptions_router,
)

router = APIRouter()

router.include_router(permanent_subscriptions_router)
router.include_router(one_time_subscriptions_router)
