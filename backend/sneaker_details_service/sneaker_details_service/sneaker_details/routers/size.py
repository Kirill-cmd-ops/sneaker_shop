from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.dependencies.get_kafka_producer import (
    get_kafka_producer,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.create_size_data import (
    send_create_size_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.delete_size_data import (
    send_delete_size_data,
)
from sneaker_details_service.sneaker_details.models import db_helper, Size
from sneaker_details_service.sneaker_details.schemas.size import SizeCreate
from sneaker_details_service.sneaker_details.services.record.create import create_record
from sneaker_details_service.sneaker_details.services.record.delete import delete_record

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sizes,
    ),
    tags=["Size"],
)


@router.post("/")
async def call_create_size(
    size_create: SizeCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        new_size = await create_record(session, Size, size_create)

    await send_create_size_data(producer, new_size.id, size_create)
    return new_size


@router.delete("/{size_id}")
async def call_delete_size(
    size_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        result = await delete_record(session, Size, size_id)

    await send_delete_size_data(producer, size_id)
    return result
