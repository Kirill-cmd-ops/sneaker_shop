from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.schemas.sneaker_sizes import (
    SneakerSizesCreate,
    SneakerSizesDelete,
    SneakerSizesRead,
)

from sneaker_details_service.sneaker_details.services.sneaker_sizes import (
    create_sneaker_sizes,
    delete_sneaker_sizes,
    read_sneaker_sizes,
)

from sneaker_details_service.sneaker_details.models.db_helper import db_helper

router = APIRouter()


@router.post("/create_sneaker_sizes/")
async def call_create_sneaker_sizes(
    sneaker_sizes_create: SneakerSizesCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker_sizes(session, sneaker_sizes_create)
    return "Запись нового размера прошла успешно"


@router.delete("/delete_sneaker_sizes/")
async def call_delete_sneaker_sizes(
    sneaker_sizes_delete: SneakerSizesDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_sizes(session, sneaker_sizes_delete)
    return "Размеры товара успешно удалены"


@router.get("/read_sneaker_sizes/", response_model=list[SneakerSizesRead])
async def call_read_sneaker_sizes(
        sneaker_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    sizes = await read_sneaker_sizes(session, sneaker_id)
    return sizes