from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.models import db_helper

from backend.core.schemas.sneaker import SneakerRead

from backend.core.services.sneaker import get_sneaker_details

router = APIRouter()


@router.get("/sneakers/")
async def call_get_sneaker_details(
    session: AsyncSession = Depends(db_helper.session_getter),
    page: Optional[int] = 1,
    limit: Optional[int] = 30,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    gender: Optional[str] = None,
    brand_name: Optional[str] = None,
    size: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc"):

    sneakers_info = await get_sneaker_details(
    session=session,
    page=page,
    limit=limit,
    name=name,
    min_price=min_price,
    max_price=max_price,
    gender=gender,
    brand_name=brand_name,
    size=size,
    sort_by=sort_by,
    order=order,
    )
    return sneakers_info
