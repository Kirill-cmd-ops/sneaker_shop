from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models.db_helper import db_helper
from sneaker_details_service.sneaker_details.services.sneaker import get_sneaker_details

from sneaker_details_service.sneaker_details.schemas.sneaker import SneakerCreate
from sneaker_details_service.sneaker_details.services.sneaker import create_sneaker

from sneaker_details_service.sneaker_details.services.sneaker import delete_sneaker

router = APIRouter()


@router.post("/create_sneaker/")
async def call_create_sneaker(
    sneaker_create: SneakerCreate,
    sneaker_quantity: int = 0,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker(session, sneaker_quantity, sneaker_create)
    return "Товар успешно создан"


@router.delete("/delete_sneaker/")
async def call_delete_sneaker(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker(session, sneaker_id)
    return "Товар успешно удален"


@router.get("/sneaker/{sneaker_id}")
async def call_get_sneaker_details(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_info = await get_sneaker_details(session=session, sneaker_id=sneaker_id)

    if not sneaker_info:
        raise HTTPException(status_code=404, detail="Кроссовки не найдены")

    return sneaker_info
