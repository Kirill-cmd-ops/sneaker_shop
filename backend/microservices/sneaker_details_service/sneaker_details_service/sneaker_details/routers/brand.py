from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.dependencies.kafka_producer import (
    get_kafka_producer,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.kafka.producers.brands import (
    publish_brand_created,
    publish_brand_deleted,
)

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import (
    db_helper,
    Brand,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import (
    BrandCreate,
    BrandResponse,
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
        settings.api.v1.brands,
    ),
    tags=["Brand"],
)


@router.post(
    "/", 
    response_model=BrandResponse, 
    status_code=status.HTTP_201_CREATED,
)
async def create_brand(
        brand_create: BrandCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> Brand:
    brand_data = brand_create.model_dump()

    new_brand = await create_record_service(
        session=session,
        table_name=Brand,
        data=brand_data,
    )

    await publish_brand_created(
        producer=producer,
        brand_id=new_brand.id,
        brand_data=brand_data,
    )
    return new_brand


@router.delete(
    "/{brand_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_brand(
        brand_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> None:
    await delete_record_service(
        session=session,
        table_name=Brand,
        record_id=brand_id,
    )

    await publish_brand_deleted(producer=producer, brand_id=brand_id)


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(
        brand_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Brand:
    brand = await get_record_service(
        session=session,
        table_name=Brand,
        record_id=brand_id,
    )
    if brand is None:
        raise HTTPException(status_code=404, detail="Бренд не найден")
    return brand
