from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.stock_notification_service.stock_notification_service.stock_notification.config import settings
from microservices.stock_notification_service.stock_notification_service.stock_notification.dependencies.user_id import (
    get_current_user_id,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.models import (
    db_helper,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.schemas.subscription import (
    SubscriptionCreate,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.subscription.one_time.deactivate import (
    deactivate_user_one_time_subscription_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.subscription.one_time.deactivate_bulk import (
    deactivate_all_one_time_subscriptions_for_user_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.subscription.one_time.fetch import (
    get_active_one_time_subscriptions_for_user_service,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.services.subscription.orchestrators import (
    create_user_one_time_subscription_orchestrator,
    reactivate_all_one_time_subscriptions_for_user_orchestrator,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.one_time_prefix,
    ),
    tags=["One Time Subscriptions"],
)


@router.post("/")
async def create_user_one_time_subscription(
        subscription_create: SubscriptionCreate,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await create_user_one_time_subscription_orchestrator(
            session=session,
            user_id=user_id,
            subscription_create=subscription_create,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Не удалось найти требуемую модель кроссовок",
        )


@router.patch("/{subscription_id}/deactivate")
async def deactivate_user_one_time_subscription(
        subscription_id: int,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await deactivate_user_one_time_subscription_service(
            subscription_id=subscription_id,
            user_id=user_id,
            session=session,
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Не удалось найти требуемую модель кроссовок",
        )


@router.patch("/deactivate")
async def deactivate_all_one_time_subscriptions_for_user(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await deactivate_all_one_time_subscriptions_for_user_service(
            user_id=user_id,
            session=session,
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Не удалось найти требуемуемые модели кроссовок",
        )


@router.patch("/{subscription_id}/reactivate")
async def reactivate_all_one_time_subscriptions_for_user(
        subscription_id: int,
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await reactivate_all_one_time_subscriptions_for_user_orchestrator(
            session=session,
            user_id=user_id,
            subscription_id=subscription_id,
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Не удалось найти требуемую модель кроссовок",
        )


@router.get("/")
async def get_active_one_time_subscriptions_for_user(
        user_id: int = Depends(get_current_user_id),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await get_active_one_time_subscriptions_for_user_service(
            user_id=user_id,
            session=session,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=404,
            detail="Не удалось найти требуемуемые модели кроссовок",
        )
