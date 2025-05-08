from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from auth.models import db_helper
from core.models import Sneaker

router = APIRouter()

@router.get("/sneakers/{sneaker_id}")
async def get_sneaker_details(sneaker_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    stmt = select(Sneaker).filter(Sneaker.id == sneaker_id).options(
        joinedload(Sneaker.brand), selectinload(Sneaker.sizes)
    )
    result = await session.execute(stmt)
    sneaker = result.scalar_one_or_none()

    if not sneaker:
        return {"error": "Кроссовок не найден"}

    return {
        "id": sneaker.id,
        "name": sneaker.name,
        "description": sneaker.description,
        "price": sneaker.price,
        "brand": {
            "id": sneaker.brand.id,
            "name": sneaker.brand.name,
            "image_url": sneaker.brand.image_url,
        },
        "sizes": [{"id": size.id, "eu_size": size.eu_size} for size in sneaker.sizes],
    }
