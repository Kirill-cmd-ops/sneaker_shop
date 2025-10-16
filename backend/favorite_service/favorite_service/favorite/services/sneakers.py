from typing import Optional

from favorite_service.favorite.models import (
    Sneaker,
    Brand,
    SneakerSizeAssociation,
    Size,
)


from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from favorite_service.favorite.schemas import (
    SneakerCreate,
    SneakerUpdate,
)


async def create_sneaker(
    session: AsyncSession,
    sneaker_create: SneakerCreate,
):
    sneaker = Sneaker(**sneaker_create.dict(exclude="size_ids"))
    session.add(sneaker)
    await session.flush()

    for size in sneaker_create.size_ids:
        sneaker_sizes = SneakerSizeAssociation(
            sneaker_id=sneaker.id, size_id=size.size_id, quantity=size.quantity
        )
        session.add(sneaker_sizes)

    await session.commit()


async def delete_sneaker(session: AsyncSession, sneaker_id: int):
    assoc_table = SneakerSizeAssociation
    stmt = delete(assoc_table).where(assoc_table.sneaker_id == sneaker_id)
    await session.execute(stmt)

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
