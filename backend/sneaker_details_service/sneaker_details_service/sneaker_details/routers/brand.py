from aiokafka import AIOKafkaProducer
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.dependencies.get_kafka_producer import (
    get_kafka_producer,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.create_brand_data import (
    send_create_brand_data,
)
from sneaker_details_service.sneaker_details.kafka.producer_event.delete_brand_data import (
    send_delete_brand_data,
)
from sneaker_details_service.sneaker_details.models import db_helper, Brand
from sneaker_details_service.sneaker_details.schemas.brand import BrandCreate
from sneaker_details_service.sneaker_details.services.record.create import create_record
from sneaker_details_service.sneaker_details.services.record.delete import delete_record

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.brands,
    ),
    tags=["Brand"],
)


@router.post("/")
async def call_create_brand(
    brand_create: BrandCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        new_brand = await create_record(session, Brand, brand_create)

    await send_create_brand_data(producer, new_brand.id, brand_create)
    return new_brand


@router.delete("/{brand_id}")
async def call_delete_brand(
    brand_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        result = await delete_record(session, Brand, brand_id)

    await send_delete_brand_data(producer, brand_id)
    return result
