from fastapi import APIRouter

from sneaker_details_service.sneaker_details.routers.sneaker import router as sneaker_details_router

router = APIRouter()

router.include_router(sneaker_details_router)