from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import SneakerMaterialAssociation
from sneaker_details_service.sneaker_details.models.db_helper import db_helper
from sneaker_details_service.sneaker_details.schemas.sneaker_association import (
    SneakerAssocsCreate,
)
from sneaker_details_service.sneaker_details.services.sneaker_association import (
    create_sneaker_association,
)

router = APIRouter()

@router.post("/create_sneaker_materials/")
async def call_create_sneaker_association(
    sneaker_associations_create: SneakerAssocsCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker_association(
        session, sneaker_associations_create, SneakerMaterialAssociation, "material_id"
    )
    return "Запись нового материала прошла успешно"
