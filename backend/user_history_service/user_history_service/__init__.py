from fastapi import APIRouter
from user_history_service.user_history.routers.check_history import router as recent_sneakers_views_router

router = APIRouter()

router.include_router(recent_sneakers_views_router)
