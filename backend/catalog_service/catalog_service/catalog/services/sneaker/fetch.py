from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from catalog_service.catalog.models import Sneaker, Brand, SneakerSizeAssociation, Size


from sqlalchemy import func, select
from sqlalchemy.orm import contains_eager, selectinload
from typing import Optional, Dict, Any


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
) -> Dict[str, Any]:
    """
    Получение списка кроссовок с фильтрацией и пагинацией.
    """
    async with session.begin():
        page = max(1, page) if page else 1
        limit = max(1, min(limit, 100)) if limit else 30
        offset = (page - 1) * limit

        stmt = (
            select(Sneaker)
            .join(Sneaker.brand)
            .where(Sneaker.is_active == True)
            .options(selectinload(Sneaker.brand))
            .options(
                selectinload(Sneaker.size_associations).joinedload(
                    SneakerSizeAssociation.size
                )
            )
        )

        if name:
            stmt = stmt.filter(Sneaker.name.ilike(f"%{name}%"))

        if min_price is not None and min_price >= 0:
            stmt = stmt.filter(Sneaker.price >= min_price)

        if max_price is not None and max_price >= 0:
            if min_price is not None and max_price < min_price:
                max_price = min_price
            stmt = stmt.filter(Sneaker.price <= max_price)

        valid_genders = {"мужские", "женские", "унисекс"}
        if gender:
            gender = gender.lower()
            if gender in valid_genders:
                stmt = stmt.filter(Sneaker.gender == gender)

        if brand_name:
            stmt = stmt.filter(Brand.name.ilike(f"%{brand_name}%"))

        if size is not None:
            size_subquery = (
                select(SneakerSizeAssociation.sneaker_id)
                .join(Size, SneakerSizeAssociation.size_id == Size.id)
                .where(Size.eu_size == size)
            ).scalar_subquery()

            stmt = stmt.filter(Sneaker.id.in_(size_subquery))

        valid_sort_columns = {"price", "created_at", "name"}
        if sort_by and sort_by in valid_sort_columns:
            sort_column = getattr(Sneaker, sort_by)
            if order and order.lower() == "desc":
                stmt = stmt.order_by(sort_column.desc())
            else:
                stmt = stmt.order_by(sort_column.asc())
        else:
            stmt = stmt.order_by(Sneaker.created_at.desc())

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count_result = await session.execute(count_stmt)
        total_count = total_count_result.scalar()

        stmt = stmt.offset(offset).limit(limit)

        result = await session.execute(stmt)
        sneakers = result.unique().scalars().all()

    return {
        "total_count": total_count,
        "items": sneakers,
    }
