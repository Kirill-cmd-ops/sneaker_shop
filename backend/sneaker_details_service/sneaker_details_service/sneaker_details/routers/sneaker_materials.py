from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.models import (
    SneakerMaterialAssociation,
    db_helper,
)
from sneaker_details_service.sneaker_details.schemas import (
    SneakerAssocsCreate,
    SneakerAssocsDelete,
    SneakerMaterialsRead,
)
from sneaker_details_service.sneaker_details.services.sneaker_association import (
    create_sneaker_association,
    delete_sneaker_association,
    read_sneaker_association,
)


router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sneaker_materials,
    ),
    tags=["Sneaker Materials"],
)


@router.post("/create/")
async def call_create_sneaker_association(
    sneaker_associations_create: SneakerAssocsCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker_association(
        session, sneaker_associations_create, SneakerMaterialAssociation, "material_id"
    )
    return "Запись нового материала прошла успешно"


@router.delete("/delete/")
async def call_delete_sneaker_association(
    sneaker_assoc_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_association(
        session, sneaker_assoc_delete, SneakerMaterialAssociation, "material_id"
    )
    return "Материалы товара успешно удалены"


@router.get("/view/", response_model=list[SneakerMaterialsRead])
async def call_read_sneaker_association(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    materials = await read_sneaker_association(
        session, SneakerMaterialAssociation, sneaker_id
    )
    return materials
