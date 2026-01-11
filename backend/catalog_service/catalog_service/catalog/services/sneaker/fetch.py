from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from catalog_service.catalog.models import Sneaker, Brand, SneakerSizeAssociation, Size


async def get_sneakers_service(
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
        .join(Brand)
        .join(SneakerSizeAssociation)
        .join(Size)
        .where(Sneaker.is_active == True)
        .distinct()
        .options(contains_eager(Sneaker.brand))
        .options(contains_eager(Sneaker.size_associations))
    )
    if name:
        stmt = stmt.filter(Sneaker.name.ilike(f"%{name}%"))

    if min_price is not None:
        stmt = stmt.filter(Sneaker.price >= min_price)

    if max_price is not None:
        stmt = stmt.filter(Sneaker.price <= max_price)

    valid_genders = {"мужские", "женские", "унисекс"}
    if gender:
        gender = gender.lower()
        if gender in valid_genders:
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

    stmt = stmt.offset(offset).limit(limit)

    result = await session.execute(stmt)
    sneakers = result.unique().scalars().all()

    count_stmt = stmt.with_only_columns(func.count(func.distinct(Sneaker.id))).order_by(
        None
    )

    result = await session.execute(count_stmt)
    total_count = result.scalar_one_or_none()

    return {
        "total_count": total_count,
        "items": sneakers,
    }
