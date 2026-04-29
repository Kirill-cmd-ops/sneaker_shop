from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper, Material
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.material import (
    MaterialCreate,
    MaterialResponse,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.create import (
    create_record_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.delete import (
    delete_record_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.materials,
    ),
    tags=["Material"],
)


@router.post(
    "/",
    response_model=MaterialResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_material(
        material_create: MaterialCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Material:
    material_data = material_create.model_dump()

    return await create_record_service(
        session=session,
        table_name=Material,
        data=material_data,
    )


@router.delete(
    "/{material_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_material(
        material_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await delete_record_service(
        session=session,
        table_name=Material,
        record_id=material_id,
    )
