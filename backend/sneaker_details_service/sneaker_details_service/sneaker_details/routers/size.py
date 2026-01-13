from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.dependencies.kafka_producer import (
    get_kafka_producer,
)
from sneaker_details_service.sneaker_details.kafka.producers.sizes import (
    publish_size_created,
    publish_size_deleted,
)

from sneaker_details_service.sneaker_details.models import db_helper, Size
from sneaker_details_service.sneaker_details.schemas.size import SizeCreate
from sneaker_details_service.sneaker_details.services.record.create import (
    create_record_service,
)
from sneaker_details_service.sneaker_details.services.record.delete import (
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
    async with session.begin():
        new_size = await create_record_service(
            session=session,
            table_name=Size,
            schema_create=size_create,
        )

    await publish_size_created(producer=producer, size_id=new_size.id, size_create=size_create)
    return new_size


@router.delete("/{size_id}")
async def delete_size(
    size_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    async with session.begin():
        result = await delete_record_service(
            session=session,
            table_name=Size,
            record_id=size_id,
        )

    await publish_size_deleted(producer=producer, size_id=size_id)
    return result
