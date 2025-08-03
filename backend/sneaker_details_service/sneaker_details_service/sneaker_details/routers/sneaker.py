from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.models.db_helper import db_helper
from sneaker_details_service.sneaker_details.services.sneaker import get_sneaker_details

router = APIRouter()


@router.get("/sneaker/{sneaker_id}")
async def call_get_sneaker_details(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_info = await get_sneaker_details(session=session, sneaker_id=sneaker_id)

    if not sneaker_info:
        raise HTTPException(status_code=404, detail="Кроссовки не найдены")

    return sneaker_info
