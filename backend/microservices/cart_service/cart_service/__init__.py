from fastapi import APIRouter

from cart_service.cart.routers.cart import router as cart_router
from cart_service.cart.routers.cart_sneaker import router as cart_sneaker_router

router = APIRouter()

router.include_router(cart_router)
router.include_router(cart_sneaker_router)