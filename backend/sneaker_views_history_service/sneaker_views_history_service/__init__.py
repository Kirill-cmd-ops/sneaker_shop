from fastapi import APIRouter
from sneaker_views_history_service.user_history.routers.get_history import router as recent_sneakers_views_router

router = APIRouter()

router.include_router(recent_sneakers_views_router)
