from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models.db_helper import db_helper
from sneaker_details_service.sneaker_details.schemas.sneaker_association import (
    SneakerAssocsCreate,
)
from sneaker_details_service.sneaker_details.services.sneaker_association import (
    create_sneaker_association,
)

from sneaker_details_service.sneaker_details.models import (
    SneakerColorAssociation,
    SneakerMaterialAssociation,
)

router = APIRouter()


@router.post("/create_sneaker_colors/")
async def call_create_sneaker_association(
    sneaker_associations_create: SneakerAssocsCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker_association(
        session, sneaker_associations_create, SneakerColorAssociation, "color_id"
    )
    return "Запись нового цвета прошла успешно"
