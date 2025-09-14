from aiokafka import AIOKafkaProducer
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings

from sneaker_details_service.sneaker_details.dependencies.get_kafka_producer import (
    get_kafka_producer,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.create_sneaker_sizes_data import (
    send_create_sneaker_sizes_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.delete_sneaker_sizes import (
    send_delete_sneaker_sizes_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.update_sneaker_sizes import (
    send_update_sneaker_sizes_data,
)
from sneaker_details_service.sneaker_details.schemas import (
    SneakerSizesCreate,
    SneakerSizesRead,
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from sneaker_details_service.sneaker_details.services.check_permissions import (
    check_role_permissions,
)

from sneaker_details_service.sneaker_details.services.sneaker_sizes import (
    create_sneaker_sizes,
    update_sneaker_sizes,
)

from sneaker_details_service.sneaker_details.models import (
    SneakerSizeAssociation,
    db_helper,
)
from sneaker_details_service.sneaker_details.services.sneaker_association import (
    delete_sneaker_association,
    read_sneaker_association,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sneaker_sizes,
    ),
    tags=["Sneaker Sizes"],
)


@router.post(
    "/create/",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.create")),),
)
async def call_create_sneaker_sizes(
    sneaker_sizes_create: SneakerSizesCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await create_sneaker_sizes(session, sneaker_sizes_create)
    await send_create_sneaker_sizes_data(producer, sneaker_sizes_create)
    return "Запись нового размера прошла успешно"


@router.delete(
    "/delete/",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.delete")),),
)
async def call_delete_sneaker_association(
    sneaker_sizes_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await delete_sneaker_association(
        session, sneaker_sizes_delete, SneakerSizeAssociation, "size_id"
    )
    await send_delete_sneaker_sizes_data(producer, sneaker_sizes_delete)
    return "Размеры товара успешно удалены"


@router.patch(
    "/update/",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.view")),),
)
async def call_update_sneaker_sizes(
    sneaker_size_update: SneakerSizeUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await update_sneaker_sizes(session, sneaker_size_update)
    await send_update_sneaker_sizes_data(producer, sneaker_size_update)
    return "Размер был изменен корректно"


@router.get(
    "/view/",
    response_model=list[SneakerSizesRead],
    dependencies=(Depends(check_role_permissions("details.sneaker.material.delete")),),
)
async def call_read_sneaker_association(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    sizes = await read_sneaker_association(session, SneakerSizeAssociation, sneaker_id)
    return sizes
