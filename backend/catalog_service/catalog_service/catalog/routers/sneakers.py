from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.catalog.models import db_helper

from catalog_service.catalog.schemas import (
    SneakerCreate,
    SneakerUpdate,
)
from catalog_service.catalog.services.sneakers import (
    get_sneakers_details,
    create_sneaker,
    delete_sneaker,
    update_sneaker,
)

router = APIRouter()


@router.post("/create_sneaker/")
async def call_create_sneaker(
    sneaker_create: SneakerCreate,
    sneaker_quantity: int = 0,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker(session, sneaker_quantity, sneaker_create)
    return "Товар успешно создан"


@router.delete("/delete_sneaker/")
async def call_delete_sneaker(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker(session, sneaker_id)
    return "Товар успешно удален"


@router.patch("/update_sneaker/")
async def call_update_sneaker(
    sneaker_id: int,
    sneaker_update: SneakerUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await update_sneaker(session, sneaker_id, sneaker_update)
    return "Товар успешно обновлен"


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
    order: Optional[str] = "asc",
):

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
