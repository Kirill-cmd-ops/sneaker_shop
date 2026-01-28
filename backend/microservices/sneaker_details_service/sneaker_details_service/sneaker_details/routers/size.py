from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.kafka_producer import (
    get_kafka_producer,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.kafka.producers.sizes import (
    publish_size_created,
    publish_size_deleted,
)

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper, Size
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.size import SizeCreate
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
        settings.api.v1.sizes,
    ),
    tags=["Size"],
)


@router.post("/")
async def create_size(
        size_create: SizeCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    new_size = await create_record_service(
        session=session,
        table_name=Size,
        schema_create=size_create,
    )

    await publish_size_created(
        producer=producer,
        size_id=new_size.id,
        size_create=size_create,
    )
    return new_size


@router.delete("/{size_id}")
async def delete_size(
        size_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    result = await delete_record_service(
        session=session,
        table_name=Size,
        record_id=size_id,
    )

    await publish_size_deleted(producer=producer, size_id=size_id)
    return result


@router.get("/{size_id}")
async def get_brand(
        size_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    return await session.scalar(select(Size.eu_size).where(Size.id == size_id))
