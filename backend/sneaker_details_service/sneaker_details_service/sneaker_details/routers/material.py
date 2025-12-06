from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import db_helper, Material
from sneaker_details_service.sneaker_details.schemas.material import MaterialCreate
from sneaker_details_service.sneaker_details.services.record import (
    create_record,
    delete_record,
)

router = APIRouter()

@router.post("/create_material/")
async def call_create_material(
    material_create: MaterialCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    new_material = await create_record(session, Material, material_create)
    return new_material


@router.delete("/delete_material/")
async def call_delete_material(
    material_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await delete_record(session, Material, material_id)
    return result
