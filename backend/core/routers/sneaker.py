from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth_servicee import db_helper
from backend.core.services.sneaker import get_sneaker_details

router = APIRouter()


@router.get("/sneaker/{sneakerId}")
async def call_get_sneaker_details(
    sneakerId: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sneaker_info = await get_sneaker_details(session=session, sneakerId=sneakerId)

    if not sneaker_info:
        raise HTTPException(status_code=404, detail="Кроссовки не найдены")

    return sneaker_info
