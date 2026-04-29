from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper, Color
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.color import (
    ColorCreate,
    ColorResponse,
)
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


@router.post(
    "/",
    response_model=ColorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_color(
        color_create: ColorCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Color:
    color_data = color_create.model_dump()

    return await create_record_service(
        session=session,
        table_name=Color,
        data=color_data,
    )


@router.delete(
    "/{color_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_color(
        color_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await delete_record_service(
        session=session,
        table_name=Color,
        record_id=color_id,
    )
