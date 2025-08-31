from fastapi import APIRouter

from catalog_service.catalog.routers.sneakers import router as catalog_router

router = APIRouter()

router.include_router(catalog_router)
