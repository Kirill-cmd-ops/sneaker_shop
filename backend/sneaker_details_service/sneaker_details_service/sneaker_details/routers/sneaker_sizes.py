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
    SneakerSizeUpdate,
    SneakerAssocsDelete,
)
from sneaker_details_service.sneaker_details.dependencies.check_permissions import (
    check_role_permissions,
)



from sneaker_details_service.sneaker_details.models import (
    SneakerSizeAssociation,
    db_helper,
)
from sneaker_details_service.sneaker_details.services.sneaker_association.delete import delete_sneaker_association
from sneaker_details_service.sneaker_details.services.sneaker_association.fetch import read_sneaker_association
from sneaker_details_service.sneaker_details.services.sneaker_size.create import create_sneaker_sizes
from sneaker_details_service.sneaker_details.services.sneaker_size.update import update_sneaker_sizes

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sneakers,
    ),
    tags=["Sneaker Sizes"],
)


@router.post(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.create")),),
)
async def call_create_sneaker_sizes(
    sneaker_id: int,
    sneaker_sizes_create: SneakerSizesCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        await create_sneaker_sizes(session, sneaker_id, sneaker_sizes_create)

    await send_create_sneaker_sizes_data(producer, sneaker_id, sneaker_sizes_create)
    return "Запись нового размера прошла успешно"


@router.delete(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.delete")),),
)
async def call_delete_sneaker_association(
    sneaker_id: int,
    sneaker_sizes_delete: SneakerAssocsDelete,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        await delete_sneaker_association(
            session,
            sneaker_id,
            sneaker_sizes_delete,
            SneakerSizeAssociation,
            "size_id",
        )

    await send_delete_sneaker_sizes_data(producer, sneaker_id, sneaker_sizes_delete)
    return "Размеры товара успешно удалены"


@router.patch(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.update")),),
)
async def call_update_sneaker_sizes(
    sneaker_id: int,
    sneaker_size_update: SneakerSizeUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        await update_sneaker_sizes(session, sneaker_id, sneaker_size_update)

    await send_update_sneaker_sizes_data(producer, sneaker_id, sneaker_size_update)
    return "Размер был изменен корректно"


@router.get(
    "/{sneaker_id}/sizes",
    dependencies=(Depends(check_role_permissions("details.sneaker.size.view")),),
)
async def call_read_sneaker_association(
    sneaker_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    async with session.begin():
        sizes = await read_sneaker_association(
            session, SneakerSizeAssociation, sneaker_id
        )
        return sizes
