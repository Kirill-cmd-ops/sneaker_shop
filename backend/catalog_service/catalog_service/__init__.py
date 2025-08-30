from fastapi import APIRouter

from catalog_service.catalog.routers.sneakers import router as catalog_router
from catalog_service.catalog.routers.sneaker_sizes import router as sneaker_sizes_router

router = APIRouter()

router.include_router(catalog_router)
router.include_router(sneaker_sizes_router)