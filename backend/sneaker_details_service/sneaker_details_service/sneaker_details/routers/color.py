from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.models import db_helper, Color
from sneaker_details_service.sneaker_details.schemas.color import ColorCreate
from sneaker_details_service.sneaker_details.services.record.create import create_record
from sneaker_details_service.sneaker_details.services.record.delete import delete_record

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.colors,
    ),
    tags=["Color"],
)

@router.post("/")
async def call_create_color(
    color_create: ColorCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    async with session.begin():
        new_color = await create_record(session, Color, color_create)
        return new_color


@router.delete("/{color_id}")
async def call_delete_color(
    color_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        result = await delete_record(session, Color, color_id)
        return result
