from fastapi.encoders import jsonable_encoder

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import SneakerCreate


async def send_create_sneaker_data(
    producer,
    sneaker_id: int,
    sneaker_create: SneakerCreate,
):
    sneaker_create_payload = {
        "event_type": "sneaker_created",
        "data": sneaker_create.dict(),
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_work_topic,
        key=str(sneaker_id),
        value=jsonable_encoder(sneaker_create_payload),
    )
