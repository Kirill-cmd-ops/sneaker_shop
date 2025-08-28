from fastapi import APIRouter

from sneaker_details_service.sneaker_details.routers.sneaker import router as sneaker_router

from sneaker_details_service.sneaker_details.routers.sneaker_sizes import router as sneaker_sizes_router


router = APIRouter()

router.include_router(sneaker_router)
router.include_router(sneaker_sizes_router)