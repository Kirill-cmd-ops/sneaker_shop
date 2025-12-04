from stock_notification_service.stock_notification.models import User

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.schemas import (
    UserCreate,
    UserUpdate,
)


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
):
    user = User(**user_create.dict())
    session.add(user)
    await session.flush()

    await session.commit()


async def delete_user(session: AsyncSession, user_id: int):
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)

    await session.commit()


async def update_user(
    session: AsyncSession, user_id: int, user_update: UserUpdate
):
    user = await session.get(User, user_id)
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    session.add(user)
    await session.commit()
