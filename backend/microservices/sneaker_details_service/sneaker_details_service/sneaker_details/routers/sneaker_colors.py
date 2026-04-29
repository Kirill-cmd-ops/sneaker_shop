from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import (
    SneakerAssocsCreate,
    SneakerColorResponse,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.permissions import (
    check_role_permissions,
)

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import (
    SneakerColorAssociation,
    db_helper,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker_association.create import (
    create_sneaker_associations_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker_association.delete import (
    delete_sneaker_associations_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.sneaker_association.fetch import (
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
    response_model=list[SneakerColorResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=(Depends(check_role_permissions("details.sneaker.color.create")),),
)
async def add_colors_to_sneaker(
        sneaker_id: int,
        sneaker_associations_create: SneakerAssocsCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> list[SneakerColorAssociation]:
    color_ids = sneaker_associations_create.assoc_ids

    return await create_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        assoc_ids=color_ids,
        sneaker_association_model=SneakerColorAssociation,
        field_name="color_id",
    )


@router.delete(
    "/{sneaker_id}/colors",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=(Depends(check_role_permissions("details.sneaker.color.delete")),),
)
async def delete_colors_from_sneaker(
        sneaker_id: int,
        color_ids: list[int],
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await delete_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        assoc_ids=color_ids,
        sneaker_association_model=SneakerColorAssociation,
        field_name="color_id",
    )


@router.get(
    "/{sneaker_id}/colors",
    response_model=list[SneakerColorResponse],
    dependencies=(Depends(check_role_permissions("details.sneaker.color.view")),),
)
async def get_sneaker_colors(
        sneaker_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> list[SneakerColorAssociation]:
    return await get_sneaker_associations_service(
        session=session,
        sneaker_association_model=SneakerColorAssociation,
        sneaker_id=sneaker_id,
    )
