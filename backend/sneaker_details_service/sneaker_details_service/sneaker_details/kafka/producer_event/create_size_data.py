from fastapi.encoders import jsonable_encoder

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import SizeCreate


async def send_create_size_data(
    producer,
    size_id: int,
    size_create: SizeCreate,
):
    size_create_payload = {
        "event_type": "size_created",
        "data": size_create.dict(),
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.size_work_topic,
        key=str(size_id),
        value=jsonable_encoder(size_create_payload),
    )
