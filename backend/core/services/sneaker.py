from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.core.models import Sneaker, Brand, SneakerSizeAssociation, Size


async def get_sneaker_details(
    session: AsyncSession,
    page: Optional[int] = 1,
    limit: Optional[int] = 30,
    name: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    gender: Optional[str] = None,
    brand_name: Optional[str] = None,
    size: Optional[float] = None,
    min_size: Optional[float] = None,
    max_size: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = "asc",
):
    offset = (page - 1) * limit

    stmt = (
        select(Sneaker)
        .distinct()
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

    valid_genders = {"Мужские", "Женские", "Унисекс"}
    if gender and gender in valid_genders:
        stmt = stmt.filter(Sneaker.gender == gender)

    if brand_name:
        stmt = stmt.filter(Brand.name.ilike(f"%{brand_name}%"))

    if size:
        stmt = stmt.filter(Size.eu_size == size)

    if min_size:
        stmt = stmt.filter(Size.eu_size >= min_size)

    if max_size:
        stmt = stmt.filter(Size.eu_size <= max_size)

    valid_sort_columns = {"price", "name", "created_at", "brand_name"}
    if sort_by and sort_by in valid_sort_columns:
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
