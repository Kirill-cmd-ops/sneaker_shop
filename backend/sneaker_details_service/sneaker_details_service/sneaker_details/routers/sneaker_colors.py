from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings

from sneaker_details_service.sneaker_details.schemas import (
    SneakerAssocsCreate,
    SneakerAssocsDelete,
)
from sneaker_details_service.sneaker_details.dependencies.check_permissions import (
    check_role_permissions,
)

from sneaker_details_service.sneaker_details.models import (
    SneakerColorAssociation,
    db_helper,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.create import create_sneaker_association
from sneaker_details_service.sneaker_details.services.sneaker_association.delete import delete_sneaker_association
from sneaker_details_service.sneaker_details.services.sneaker_association.fetch import read_sneaker_association

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sneakers,
    ),
    tags=["Sneaker Colors"],
)


@router.post(
    "/{sneaker_id}/colors",
    dependencies=(Depends(check_role_permissions("details.sneaker.color.create")),),
)
async def call_create_sneaker_association(
    sneaker_id: int,
    sneaker_associations_create: SneakerAssocsCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        await create_sneaker_association(
            session,
            sneaker_id,
            sneaker_associations_create,
            SneakerColorAssociation,
            "color_id",
        )
        return "Запись нового цвета прошла успешно"


@router.delete(
    "/{sneaker_id}/colors",
    dependencies=(Depends(check_role_permissions("details.sneaker.color.delete")),),
)
async def call_delete_sneaker_association(
    sneaker_id: int,
    sneaker_assoc_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        await delete_sneaker_association(
            session,
            sneaker_id,
            sneaker_assoc_delete,
            SneakerColorAssociation,
            "color_id",
        )
        return "Цвета товара успешно удалены"


@router.get(
    "/{sneaker_id}/colors",
    dependencies=(Depends(check_role_permissions("details.sneaker.color.view")),),
)
async def call_read_sneaker_association(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        colors = await read_sneaker_association(
            session, SneakerColorAssociation, sneaker_id
        )
        return colors
