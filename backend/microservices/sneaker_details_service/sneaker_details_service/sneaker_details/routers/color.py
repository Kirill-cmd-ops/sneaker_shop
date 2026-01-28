from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper, Color
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.color import ColorCreate
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
        settings.api.v1.colors,
    ),
    tags=["Color"],
)


@router.post("/")
async def create_color(
        color_create: ColorCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await create_record_service(
        session=session,
        table_name=Color,
        schema_create=color_create,
    )


@router.delete("/{color_id}")
async def delete_color(
        color_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await delete_record_service(
        session=session,
        table_name=Color,
        record_id=color_id,
    )
