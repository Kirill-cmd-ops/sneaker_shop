from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import SneakerMaterialAssociation
from sneaker_details_service.sneaker_details.models import Sneaker
from sneaker_details_service.sneaker_details.models import Material
import random

async def seed_sneaker_materials(db: AsyncSession):
    sneakers = (await db.execute(select(Sneaker))).scalars().all()
    materials = (await db.execute(select(Material))).scalars().all()

    associations = []

    for sneaker in sneakers:
        assigned_materials = random.sample(materials, min(3, len(materials)))

        for material in assigned_materials:
            associations.append(
                SneakerMaterialAssociation(sneaker_id=sneaker.id, material_id=material.id)
            )

    db.add_all(associations)
    await db.commit()
