from fastapi import APIRouter

from sneaker_details_service.sneaker_details.routers.sneaker import router as sneaker_router

from sneaker_details_service.sneaker_details.routers.sneaker_sizes import router as sneaker_sizes_router
from sneaker_details_service.sneaker_details.routers.sneaker_colors import router as sneaker_colors_router
from sneaker_details_service.sneaker_details.routers.sneaker_materials import router as sneaker_materials_router

from sneaker_details_service.sneaker_details.routers.brand import router as brand_router
from sneaker_details_service.sneaker_details.routers.color import router as color_router
from sneaker_details_service.sneaker_details.routers.country import router as country_router
from sneaker_details_service.sneaker_details.routers.material import router as material_router
from sneaker_details_service.sneaker_details.routers.size import router as size_router


router = APIRouter()

router.include_router(sneaker_router)
router.include_router(sneaker_sizes_router)
router.include_router(sneaker_colors_router)
router.include_router(sneaker_materials_router)
router.include_router(brand_router)
router.include_router(color_router)
router.include_router(country_router)
router.include_router(material_router)
router.include_router(size_router)