from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.models import db_helper, Material
from sneaker_details_service.sneaker_details.schemas.material import MaterialCreate
from sneaker_details_service.sneaker_details.services.record.create import (
    create_record_service,
)
from sneaker_details_service.sneaker_details.services.record.delete import (
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


@router.post("/")
async def create_material(
    material_create: MaterialCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        new_material = await create_record_service(
            session=session,
            table_name=Material,
            schema_create=material_create,
        )
        return new_material


@router.delete("/{material_id}")
async def delete_material(
    material_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        result = await delete_record_service(
            session=session,
            table_name=Material,
            record_id=material_id,
        )
        return result
