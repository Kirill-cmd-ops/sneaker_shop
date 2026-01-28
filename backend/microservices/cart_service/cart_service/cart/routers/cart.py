from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.config import settings
from microservices.cart_service.cart_service.cart.models import db_helper
from microservices.cart_service.cart_service.cart.dependencies.user_id import get_current_user_id
from microservices.cart_service.cart_service.cart.services.cart.delete import delete_cart_service
from microservices.cart_service.cart_service.cart.services.cart.orchestrators import get_cart_orchestrator

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Cart"],
)


@router.get("/")
async def get_cart(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_cart_orchestrator(
        session=session,
        user_id=user_id,
    )


@router.delete("/")
async def delete_cart(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await delete_cart_service(
        session=session,
        user_id=user_id,
    )
