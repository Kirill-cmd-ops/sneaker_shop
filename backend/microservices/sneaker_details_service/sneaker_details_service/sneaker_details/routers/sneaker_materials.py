from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import (
    SneakerMaterialAssociation,
    db_helper,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import (
    SneakerAssocsCreate,
    SneakerMaterialResponse,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.permissions import (
    check_role_permissions,
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
    tags=["Sneaker Materials"],
)


@router.post(
    "/{sneaker_id}/materials",
    response_model=list[SneakerMaterialResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=(Depends(check_role_permissions("details.sneaker.material.create")),),
)
async def add_materials_to_sneaker(
        sneaker_id: int,
        sneaker_associations_create: SneakerAssocsCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> list[SneakerMaterialAssociation]:
    material_ids = sneaker_associations_create.assoc_ids

    return await create_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        assoc_ids=material_ids,
        sneaker_association_model=SneakerMaterialAssociation,
        field_name="material_id",
    )


@router.delete(
    "/{sneaker_id}/materials",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=(Depends(check_role_permissions("details.sneaker.material.delete")),),
)
async def delete_materials_from_sneaker(
        sneaker_id: int,
        material_ids: list[int],
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await delete_sneaker_associations_service(
        session=session,
        sneaker_id=sneaker_id,
        assoc_ids=material_ids,
        sneaker_association_model=SneakerMaterialAssociation,
        field_name="material_id",
    )


@router.get(
    "/{sneaker_id}/materials",
    response_model=list[SneakerMaterialResponse],
    dependencies=(Depends(check_role_permissions("details.sneaker.material.view")),),
)
async def get_sneaker_materials(
        sneaker_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> list[SneakerMaterialAssociation]:
    return await get_sneaker_associations_service(
        session=session,
        sneaker_association_model=SneakerMaterialAssociation,
        sneaker_id=sneaker_id,
    )
