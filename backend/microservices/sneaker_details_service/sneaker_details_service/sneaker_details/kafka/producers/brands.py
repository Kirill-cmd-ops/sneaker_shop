from fastapi.encoders import jsonable_encoder

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import BrandCreate


async def publish_brand_created(
        producer,
        brand_id: int,
        brand_create: BrandCreate,
):
    brand_create_payload = {
        "event_type": "brand_created",
        "data": brand_create.dict(),
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.brand_work_topic,
        key=str(brand_id),
        value=jsonable_encoder(brand_create_payload),
    )


async def publish_brand_deleted(producer, brand_id: int):
    brand_delete_payload = {
        "event_type": "brand_deleted",
        "brand_id": brand_id,
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.brand_work_topic,
        key=str(brand_id),
        value=brand_delete_payload,
    )
