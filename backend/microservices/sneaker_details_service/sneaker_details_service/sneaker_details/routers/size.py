from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException, status
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
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas.size import (
    SizeCreate,
    SizeResponse,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.create import (
    create_record_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.delete import (
    delete_record_service,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.services.record.fetch import (
    get_record_service,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.sizes,
    ),
    tags=["Size"],
)


@router.post(
    "/",
    response_model=SizeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_size(
        size_create: SizeCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> Size:
    size_data = size_create.model_dump()

    new_size = await create_record_service(
        session=session,
        table_name=Size,
        data=size_data,
    )

    await publish_size_created(
        producer=producer,
        size_id=new_size.id,
        size_data=size_data,
    )
    return new_size


@router.delete(
    "/{size_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_size(
        size_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> None:
    await delete_record_service(
        session=session,
        table_name=Size,
        record_id=size_id,
    )

    await publish_size_deleted(producer=producer, size_id=size_id)


@router.get("/{size_id}", response_model=SizeResponse)
async def get_size(
        size_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Size:
    size = await get_record_service(
        session=session,
        table_name=Size,
        record_id=size_id,
    )
    if size is None:
        raise HTTPException(status_code=404, detail="Размер не найден")
    return size
