from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.dependencies.get_kafka_producer import get_kafka_producer
from sneaker_details_service.sneaker_details.kafka.producer_event.create_size_data import (
    send_create_size_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.delete_size_data import send_delete_size_data
from sneaker_details_service.sneaker_details.models import db_helper, Size
from sneaker_details_service.sneaker_details.schemas.size import SizeCreate
from sneaker_details_service.sneaker_details.services.record import (
    create_record,
    delete_record,
)

router = APIRouter()


@router.post("/create_size/")
async def call_create_size(
    size_create: SizeCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    new_size = await create_record(session, Size, size_create)
    await send_create_size_data(producer, new_size.id, size_create)

    return new_size


@router.delete("/delete_size/")
async def call_delete_size(
    size_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    result = await delete_record(session, Size, size_id)
    await send_delete_size_data(producer, size_id)

    return result
