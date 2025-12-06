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
        settings.api.v1.sneaker,
    ),
    tags=["Sneaker Stock Notification"],
)


@router.post("/add/")
async def call_add_user_subscriptions(
    sneaker_id: int,
    size_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        result = await add_user_subscriptions(
            sneaker_id=sneaker_id,
            size_id=size_id,
            user_id=user_id,
            session=session,
        )
        return result

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=404, detail="Не удалось найти требуемую модель кроссовок"
        )


@router.delete("/delete/")
async def call_delete_user_subscriptions(
    sneaker_id: int,
    size_id: int,
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        result = await delete_user_subscriptions(
            sneaker_id=sneaker_id,
            size_id=size_id,
            user_id=user_id,
            session=session,
        )
        return result

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=404, detail="Не удалось найти требуемую модель кроссовок"
        )


@router.delete("/all/delete/")
async def call_delete_all_user_subscriptions(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        result = await delete_all_user_subscriptions(
            user_id=user_id,
            session=session,
        )
        return result

    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=404, detail="Не удалось найти требуемуемые модели кроссовок"
        )


@router.get("/view/")
async def call_get_user_subscriptions_for_notifications(
    user_id: int = Depends(get_user_by_header),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        result = await get_user_subscriptions_for_notifications(
            user_id=user_id,
            session=session,
        )
        return result
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=404, detail="Не удалось найти требуемуемые модели кроссовок"
        )
