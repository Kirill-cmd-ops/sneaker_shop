from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models import db_helper, Color
from sneaker_details_service.sneaker_details.schemas.color import ColorCreate
from sneaker_details_service.sneaker_details.services.record import (
    create_record,
    delete_record,
)

router = APIRouter()

@router.post("/create_color/")
async def call_create_color(
    color_create: ColorCreate, session: AsyncSession = Depends(db_helper.session_getter)
):
    new_color = await create_record(session, Color, color_create)
    return new_color


@router.delete("/delete_color/")
async def call_delete_color(
    color_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await delete_record(session, Color, color_id)

    return result
