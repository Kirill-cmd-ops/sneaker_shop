from typing import Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.cart_service.cart_service.cart.config import settings
from microservices.cart_service.cart_service.cart.models import db_helper
from microservices.cart_service.cart_service.cart.schemas import CartResponse
from microservices.cart_service.cart_service.cart.dependencies.user_id import get_current_user_id
from microservices.cart_service.cart_service.cart.services.cart.delete import delete_cart_service
from microservices.cart_service.cart_service.cart.services.cart.orchestrators import get_cart_orchestrator

router = APIRouter(
    prefix=settings.api.build_path(settings.api.root, settings.api.v1.prefix),
    tags=["Cart"],
)


@router.get("/", response_model=CartResponse)
async def get_cart(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> dict[str, Any]:
    return await get_cart_orchestrator(
        session=session,
        user_id=user_id,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_cart(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await delete_cart_service(
        session=session,
        user_id=user_id,
    )
