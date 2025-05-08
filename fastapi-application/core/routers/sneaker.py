from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from auth.models import db_helper
from core.models import Sneaker, Brand, SneakerSizeAssociation, Size
from core.schemas.sneaker import SneakerRead

router = APIRouter()


@router.get("/sneakers/", response_model=list[SneakerRead])
async def get_sneaker_details(
    page: Optional[int] = 1,
    limit: Optional[int] = 30,
    name: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    brand_name: Optional[str] = None,
    size: Optional[float] = None,
    min_size: Optional[float] = None,
    max_size: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
    session: AsyncSession = Depends(db_helper.session_getter),
):
    offset = (page - 1) * limit

    stmt = (
        select(Sneaker)
        .group_by(Sneaker.id)
        .join(Brand)
        .join(SneakerSizeAssociation)
        .join(Size)
        .where(Sneaker.is_active == True)
    )

    if name:
        stmt = stmt.filter(Sneaker.name.ilike(f"%{name}%"))

    if min_price is not None:
        stmt = stmt.filter(Sneaker.price >= min_price)

    if max_price is not None:
        stmt = stmt.filter(Sneaker.price <= max_price)

    if brand_name:
        stmt = stmt.filter(Brand.name.ilike(f"%{brand_name}%"))

    if size:
        stmt = stmt.filter(Size.eu_size == size)

    if min_size:
        stmt = stmt.filter(Size.eu_size >= min_size)

    if max_size:
        stmt = stmt.filter(Size.eu_size <= max_size)

    if sort_by:
        if sort_by == "brand_name":
            sort_column = Brand.name
        else:
            sort_column = getattr(Sneaker, sort_by, None)

        if sort_column:
            stmt = stmt.order_by(
                sort_column.desc() if order == "desc" else sort_column.asc()
            )

    stmt = stmt.offset(offset).limit(limit).options(
        joinedload(Sneaker.brand), selectinload(Sneaker.sizes)
    )

    result = await session.execute(stmt)
    sneakers = result.scalars().all()

    return sneakers
