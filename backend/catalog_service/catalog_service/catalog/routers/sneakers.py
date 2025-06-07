from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.catalog.services.sneakers import get_sneakers_details
from catalog_service.catalog.models.db_helper import db_helper


router = APIRouter()


@router.get("/sneakers/")
async def call_get_sneakers_details(
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

    sneakers_info = await get_sneakers_details(
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
