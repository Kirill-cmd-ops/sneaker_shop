from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.catalog.schemas import (
    SneakerSizesCreate,
    SneakerSizesRead,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)

from catalog_service.catalog.services.sneaker_sizes import (
    create_sneaker_sizes,
    update_sneaker_sizes,
)

from catalog_service.catalog.models import db_helper, SneakerSizeAssociation

from catalog_service.catalog.services.sneaker_association import (
    delete_sneaker_association,
    read_sneaker_association,
)

router = APIRouter()


@router.post("/create_sneaker_sizes/")
async def call_create_sneaker_sizes(
    sneaker_sizes_create: SneakerSizesCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await create_sneaker_sizes(session, sneaker_sizes_create)
    return "Запись нового размера прошла успешно"


@router.delete("/delete_sneaker_sizes/")
async def call_delete_sneaker_association(
    sneaker_sizes_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_association(
        session, sneaker_sizes_delete, SneakerSizeAssociation, "size_id"
    )
    return "Размеры товара успешно удалены"


@router.get("/read_sneaker_sizes/", response_model=list[SneakerSizesRead])
async def call_read_sneaker_association(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sizes = await read_sneaker_association(session, SneakerSizeAssociation, sneaker_id)
    return sizes


@router.patch("/update_sneaker_sizes/")
async def call_update_sneaker_sizes(
    sneaker_size_update: SneakerSizeUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await update_sneaker_sizes(session, sneaker_size_update)
    return "Размер был изменен корректно"
