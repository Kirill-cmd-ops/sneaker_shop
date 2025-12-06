from fastapi.encoders import jsonable_encoder

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import BrandCreate


async def send_create_brand_data(
    producer,
    brand_id: int,
    brand_create: BrandCreate,
):
    brand_create_payload = {
        "event_type": "brand_created",
        "data": brand_create.dict(),
    }

    await producer.send_and_wait(
        settings.kafka_config.brand_work_topic,
        key=str(brand_id),
        value=jsonable_encoder(brand_create_payload),
    )
