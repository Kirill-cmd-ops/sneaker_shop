from aiokafka import AIOKafkaProducer
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.kafka_producer import (
    get_kafka_producer,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.kafka.producers.brands import (
    publish_brand_created,
    publish_brand_deleted,
)

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper, Brand
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.brand import BrandCreate
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.create import (
    create_record_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.delete import (
    delete_record_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.brands,
    ),
    tags=["Brand"],
)


@router.post("/")
async def create_brand(
        brand_create: BrandCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    new_brand = await create_record_service(
        session=session,
        table_name=Brand,
        schema_create=brand_create,
    )

    await publish_brand_created(
        producer=producer,
        brand_id=new_brand.id,
        brand_create=brand_create,
    )
    return new_brand


@router.delete("/{brand_id}")
async def delete_brand(
        brand_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    result = await delete_record_service(
        session=session,
        table_name=Brand,
        record_id=brand_id,
    )

    await publish_brand_deleted(producer=producer, brand_id=brand_id)
    return result


@router.get("/{brand_id}")
async def get_brand(
        brand_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await session.scalar(select(Brand.name).where(Brand.id == brand_id))
