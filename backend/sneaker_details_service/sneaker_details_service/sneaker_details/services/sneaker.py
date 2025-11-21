from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, contains_eager

from sneaker_details_service.sneaker_details.schemas import (
    SneakerCreate,
    SneakerUpdate,
)

from sneaker_details_service.sneaker_details.models import (
    SneakerColorAssociation,
    SneakerMaterialAssociation,
    SneakerSizeAssociation,
    Sneaker,
)


async def create_sneaker(
    session: AsyncSession,
    sneaker_create: SneakerCreate,
):
    sneaker = Sneaker(
        **sneaker_create.dict(exclude={"size_ids", "color_ids", "material_ids"})
    )
    session.add(sneaker)
    await session.flush()

    for size in sneaker_create.size_ids:
        sneaker_sizes = SneakerSizeAssociation(
            sneaker_id=sneaker.id, size_id=size.size_id, quantity=size.quantity
        )
        session.add(sneaker_sizes)
    for color_id in sneaker_create.color_ids:
        sneaker_colors = SneakerColorAssociation(
            sneaker_id=sneaker.id, color_id=color_id
        )
        session.add(sneaker_colors)
    for material_id in sneaker_create.material_ids:
        sneaker_materials = SneakerMaterialAssociation(
            sneaker_id=sneaker.id, material_id=material_id
        )
        session.add(sneaker_materials)

    await session.commit()
    return sneaker


async def delete_sneaker(session: AsyncSession, sneaker_id: int):
    assoc_tables = [
        SneakerSizeAssociation,
        SneakerColorAssociation,
        SneakerMaterialAssociation,
    ]
    for assoc_table in assoc_tables:
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


async def get_sneaker_details(
    session: AsyncSession,
    sneaker_id: int,
):
    stmt = (
        select(Sneaker)
        .where(Sneaker.id == sneaker_id)
        .where(Sneaker.is_active == True)
        .options(
            joinedload(Sneaker.brand),
            joinedload(Sneaker.country),
            selectinload(Sneaker.sizes),
            selectinload(Sneaker.colors),
            selectinload(Sneaker.materials),
        )
    )
    result = await session.execute(stmt)
    sneaker = result.unique().scalar_one_or_none()
    return sneaker
