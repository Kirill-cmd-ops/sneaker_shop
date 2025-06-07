from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from catalog_service.catalog.models import Sneaker, Brand, SneakerSizeAssociation, Size


async def get_sneakers_details(
    session: AsyncSession,
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

    valid_sort_columns = {"price", "created_at"}
    if sort_by and sort_by in valid_sort_columns:
        sort_column = getattr(Sneaker, sort_by, None)

        if sort_column:
            stmt = stmt.order_by(
                sort_column.desc() if order == "desc" else sort_column.asc()
            )

    count_stmt = stmt.with_only_columns(func.count(func.distinct(Sneaker.id))).order_by(
        None
    )

    result = await session.execute(count_stmt)
    total_count = result.scalar_one_or_none()

    stmt = (
        stmt.offset(offset)
        .limit(limit)
        .options(
            joinedload(Sneaker.brand),
            selectinload(Sneaker.sizes),
        )
    )

    result = await session.execute(stmt)
    sneakers = result.scalars().all()

    return {
        "total_count": total_count,
        "items": sneakers,
    }
