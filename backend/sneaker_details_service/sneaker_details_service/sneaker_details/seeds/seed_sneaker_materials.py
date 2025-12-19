from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import (
    SneakerMaterialAssociation,
    Sneaker,
    Material,
)
import random


async def seed_sneaker_materials(session: AsyncSession):
    sneakers = (await session.execute(select(Sneaker))).scalars().all()
    materials = (await session.execute(select(Material))).scalars().all()

    associations = []

    for sneaker in sneakers:
        assigned_materials = random.sample(materials, min(3, len(materials)))

        for material in assigned_materials:
            associations.append(
                {"sneaker_id": sneaker.id, "material_id": material.id},
            )

    stmt = insert(SneakerMaterialAssociation).values(associations)
    await session.execute(stmt)
    await session.commit()
