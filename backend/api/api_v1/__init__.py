from fastapi import APIRouter

from auth_service.auth.authentication.routers import router as auth_router
from auth_service.auth.authentication.users import router as users_router
from backend.core.routers.sneakers import router as sneakers_router
from backend.core.routers.sneaker import router as sneaker_router
from auth_service.profile.routers.profile import router as profile_router
from backend.core.routers.cart import router as cart_router
from backend.core.routers.cart_sneaker import router as cart_sneaker_router
from favorite_service.favorite.routers.favorite import router as favorite_router
from favorite_service.favorite.routers.favorite_sneaker import router as favorite_sneaker_router
from auth_service.auth.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(auth_router)

router.include_router(users_router)

router.include_router(sneakers_router)

router.include_router(sneaker_router)

router.include_router(profile_router)

router.include_router(cart_router)

router.include_router(cart_sneaker_router)

router.include_router(favorite_router)

router.include_router(favorite_sneaker_router)