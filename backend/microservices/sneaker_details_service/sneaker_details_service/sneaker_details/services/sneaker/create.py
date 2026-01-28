from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import (
    Sneaker,
    SneakerSizeAssociation,
    SneakerColorAssociation,
    SneakerMaterialAssociation,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import SneakerCreate


async def create_sneaker_service(
        session: AsyncSession,
        sneaker_create: SneakerCreate,
):
    async with session.begin():
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

    return sneaker
