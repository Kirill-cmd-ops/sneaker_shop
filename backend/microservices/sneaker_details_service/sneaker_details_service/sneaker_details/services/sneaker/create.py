from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import (
    Sneaker,
    SneakerSizeAssociation,
    SneakerColorAssociation,
    SneakerMaterialAssociation,
)


# TODO: добавить DomainException
async def create_sneaker_service(
        session: AsyncSession,
        sneaker_data: Dict[str, Any],
        size_ids: list[Dict[str, Any]],
        color_ids: list[int],
        material_ids: list[int],
):
    async with session.begin():
        sneaker = Sneaker(**sneaker_data)
        session.add(sneaker)
        await session.flush()

        for size in size_ids:
            sneaker_sizes = SneakerSizeAssociation(
                sneaker_id=sneaker.id, size_id=size["size_id"], quantity=size["quantity"],
            )
            session.add(sneaker_sizes)
        for color_id in color_ids:
            sneaker_colors = SneakerColorAssociation(
                sneaker_id=sneaker.id, color_id=color_id
            )
            session.add(sneaker_colors)
        for material_id in material_ids:
            sneaker_materials = SneakerMaterialAssociation(
                sneaker_id=sneaker.id, material_id=material_id
            )
            session.add(sneaker_materials)

    return sneaker
