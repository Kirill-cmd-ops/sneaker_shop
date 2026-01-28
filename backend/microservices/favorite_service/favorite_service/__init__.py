from fastapi import APIRouter

from microservices.favorite_service.favorite_service.favorite.routers.favorite import router as favorite_router
from microservices.favorite_service.favorite_service.favorite.routers.favorite_sneaker import \
    router as favorite_sneaker_router

router = APIRouter()

router.include_router(favorite_router)
router.include_router(favorite_sneaker_router)
