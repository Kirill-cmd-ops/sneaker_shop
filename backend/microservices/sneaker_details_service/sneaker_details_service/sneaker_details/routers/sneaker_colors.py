from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings

from sneaker_details_service.sneaker_details.schemas import (
    SneakerAssocsCreate,
    SneakerAssocsDelete,
)
from sneaker_details_service.sneaker_details.dependencies.permissions import (
    check_role_permissions,
)

from sneaker_details_service.sneaker_details.models import (
    SneakerColorAssociation,
    db_helper,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.create import (
    create_sneaker_associations_service,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.delete import (
    delete_sneaker_associations_service,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.fetch import (
    get_sneaker_associations_service,
)

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
async def add_colors_to_sneaker(
    sneaker_id: int,
    sneaker_associations_create: SneakerAssocsCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        sneaker_associations_create=sneaker_associations_create,
        sneaker_association_model=SneakerColorAssociation,
        field_name="color_id",
    )
    return "Запись нового цвета прошла успешно"


@router.delete(
    "/{sneaker_id}/colors",
    dependencies=(Depends(check_role_permissions("details.sneaker.color.delete")),),
)
async def delete_colors_from_sneaker(
    sneaker_id: int,
    sneaker_assoc_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        sneaker_assoc_delete=sneaker_assoc_delete,
        sneaker_association_model=SneakerColorAssociation,
        field_name="color_id",
    )
    return "Цвета товара успешно удалены"


@router.get(
    "/{sneaker_id}/colors",
    dependencies=(Depends(check_role_permissions("details.sneaker.color.view")),),
)
async def get_sneaker_colors(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_sneaker_associations_service(
        session=session,
        sneaker_association_model=SneakerColorAssociation,
        sneaker_id=sneaker_id,
    )
