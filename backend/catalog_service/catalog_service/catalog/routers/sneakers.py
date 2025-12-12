from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.catalog.config import settings
from catalog_service.catalog.models import db_helper


from catalog_service.catalog.services.sneakers import (
    get_sneakers_details,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
    ),
    tags=["Catalog"],
)


@router.get("/")
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
    order: Optional[str] = "asc",
):
    async with session.begin():
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
