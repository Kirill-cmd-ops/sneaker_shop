from fastapi import HTTPException

from stock_notification_service.stock_notification.models import Sneaker

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.schemas import (
    SneakerCreate,
    SneakerUpdate,
)


async def create_sneaker(
    session: AsyncSession,
    sneaker_create: SneakerCreate,
):
    sneaker = Sneaker(**sneaker_create.dict())
    session.add(sneaker)
    await session.flush()

    await session.commit()


async def delete_sneaker(session: AsyncSession, sneaker_id: int):
    stmt = delete(Sneaker).where(Sneaker.id == sneaker_id)
    await session.execute(stmt)

    await session.commit()


async def update_sneaker(
    session: AsyncSession, sneaker_id: int, sneaker_update: SneakerUpdate
):
    sneaker = await session.get(Sneaker, sneaker_id)
    update_data = sneaker_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sneaker, field, value)

    session.add(sneaker)
    await session.commit()


async def is_sneaker_active(
    session: AsyncSession,
    sneaker_id: int,
):
    current_sneaker = await session.get(Sneaker, sneaker_id)
    if not current_sneaker.is_active:
        raise HTTPException(
            status_code=404,
            detail="Данный товар неактивен, подписка невозможна",
        )
