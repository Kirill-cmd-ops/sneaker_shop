from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.config import settings
from stock_notification_service.stock_notification.dependencies.user_id import (
    get_current_user_id,
)
from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.schemas.subscription import (
    SubscriptionCreate,
)
from stock_notification_service.stock_notification.services.sneaker.checkers import (
    check_sneaker_active_service,
)
from stock_notification_service.stock_notification.services.sneaker_size.checkers import (
    check_inactive_sneaker_size_service,
)
from stock_notification_service.stock_notification.services.subscription.one_time.checkers import (
    check_active_one_time_subscription_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.checkers import (
    check_active_permanent_subscription_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.create import (
    create_user_permanent_subscription_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.deactivate import (
    deactivate_user_permanent_subscription_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.deactivate_bulk import (
    deactivate_all_permanent_subscriptions_for_user_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.fetch import (
    get_active_permanent_subscriptions_for_user_service,
    get_inactive_permanent_subscription_for_user_service,
)
from stock_notification_service.stock_notification.services.subscription.permanent.reactivate import (
    reactivate_permanent_subscription_by_id_service,
    reactivate_permanent_subscription_by_sneaker_size_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.permanent_prefix,
    ),
    tags=["Subscriptions"],
)


@router.post("/")
async def create_user_permanent_subscription(
    subscription_create: SubscriptionCreate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            # проверка активности sneaker
            await check_sneaker_active_service(
                session=session,
                sneaker_id=subscription_create.sneaker_id,
            )

            # проверка доступности размера для sneaker и проверка что размер на данный момент неактивен
            await check_inactive_sneaker_size_service(
                session=session,
                sneaker_id=subscription_create.sneaker_id,
                size_id=subscription_create.size_id,
            )

            # проверка активной перманентной подписки
            await check_active_permanent_subscription_service(
                session=session,
                user_id=user_id,
                sneaker_id=subscription_create.sneaker_id,
                size_id=subscription_create.size_id,
            )

            # проверка активности одноразовой подписки
            await check_active_one_time_subscription_service(
                session=session,
                user_id=user_id,
                sneaker_id=subscription_create.sneaker_id,
                size_id=subscription_create.size_id,
            )

            # реактивация деактивной перманентной подписки
            update_subscription = (
                await reactivate_permanent_subscription_by_sneaker_size_service(
                    session=session,
                    user_id=user_id,
                    sneaker_id=subscription_create.sneaker_id,
                    size_id=subscription_create.size_id,
                )
            )
            if update_subscription:
                return update_subscription

            # создание перманентной подписки
            return await create_user_permanent_subscription_service(
                sneaker_id=subscription_create.sneaker_id,
                size_id=subscription_create.size_id,
                user_id=user_id,
                session=session,
            )

        except IntegrityError as e:
            raise HTTPException(
                status_code=404,
                detail="Не удалось найти требуемую модель кроссовок",
            )


@router.patch("/{subscription_id}/deactivate")
async def deactivate_user_permanent_subscription(
    subscription_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            return await deactivate_user_permanent_subscription_service(
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
async def deactivate_all_permanent_subscriptions_for_user(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            return deactivate_all_permanent_subscriptions_for_user_service(
                user_id=user_id,
                session=session,
            )

        except IntegrityError as e:
            raise HTTPException(
                status_code=404,
                detail="Не удалось найти требуемуемые модели кроссовок",
            )


@router.patch("/{subscription_id}/reactivate")
async def reactivate_all_permanent_subscriptions_for_user(
    subscription_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        inactive_subscription = (
            await get_inactive_permanent_subscription_for_user_service(
                session=session,
                user_id=user_id,
                subscription_id=subscription_id,
            )
        )

        await check_active_permanent_subscription_service(
            session=session,
            user_id=user_id,
            sneaker_id=inactive_subscription.sneaker_id,
            size_id=inactive_subscription.size_id,
        )

        await check_active_one_time_subscription_service(
            session=session,
            user_id=user_id,
            sneaker_id=inactive_subscription.sneaker_id,
            size_id=inactive_subscription.size_id,
        )

        try:
            return await reactivate_permanent_subscription_by_id_service(
                subscription_id=subscription_id,
                user_id=user_id,
                session=session,
            )

        except IntegrityError as e:
            raise HTTPException(
                status_code=404,
                detail="Не удалось найти требуемую модель кроссовок",
            )


@router.get("/")
async def get_active_permanent_subscriptions_for_user(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            return await get_active_permanent_subscriptions_for_user_service(
                user_id=user_id,
                session=session,
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=404,
                detail="Не удалось найти требуемуемые модели кроссовок",
            )
