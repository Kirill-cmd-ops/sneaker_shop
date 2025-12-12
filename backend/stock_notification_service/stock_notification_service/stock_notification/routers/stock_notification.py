from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.config import settings
from stock_notification_service.stock_notification.dependencies.get_current_user import (
    get_user_by_header,
)
from stock_notification_service.stock_notification.models import (
    db_helper,
)
from stock_notification_service.stock_notification.schemas.subscription import (
    SubscriptionCreate,
)
from stock_notification_service.stock_notification.services.stock_notification import (
    add_user_subscriptions,
    delete_user_subscriptions,
    delete_all_user_subscriptions,
    get_user_subscriptions_for_notifications,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
    ),
    tags=["Sneaker Stock Notification"],
)


@router.post("/")
async def call_add_user_subscriptions(
    subscription_create: SubscriptionCreate,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            result = await add_user_subscriptions(
                subscription_create=subscription_create,
                user_id=user_id,
                session=session,
            )
            return result

        except IntegrityError as e:
            raise HTTPException(
                status_code=404, detail="Не удалось найти требуемую модель кроссовок"
            )


@router.delete("/{subscription_id}")
async def call_delete_user_subscriptions(
    subscription_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            result = await delete_user_subscriptions(
                subscription_id=subscription_id, user_id=user_id, session=session
            )
            return result

        except IntegrityError as e:
            raise HTTPException(
                status_code=404, detail="Не удалось найти требуемую модель кроссовок"
            )


@router.delete("/")
async def call_delete_all_user_subscriptions(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            result = await delete_all_user_subscriptions(
                user_id=user_id,
                session=session,
            )
            return result

        except IntegrityError as e:
            raise HTTPException(
                status_code=404, detail="Не удалось найти требуемуемые модели кроссовок"
            )


@router.get("/")
async def call_get_user_subscriptions_for_notifications(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        try:
            result = await get_user_subscriptions_for_notifications(
                user_id=user_id,
                session=session,
            )
            return result
        except IntegrityError as e:
            raise HTTPException(
                status_code=404, detail="Не удалось найти требуемуемые модели кроссовок"
            )
