from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import SneakerSizesCreate


async def send_create_sneaker_sizes_data(
    producer,
    sneaker_sizes_create: SneakerSizesCreate,
):
    sneaker_sizes_create_payload = {
        "event_type": "sneaker_sizes_created",
        "data": sneaker_sizes_create.dict(),
    }
    await producer.send_and_wait(
        settings.kafka_config.sneaker_topic,
        key=str(sneaker_sizes_create.sneaker_id),
        value=sneaker_sizes_create_payload,
    )