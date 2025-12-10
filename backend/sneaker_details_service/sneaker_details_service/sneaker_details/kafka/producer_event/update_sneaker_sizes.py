from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import SneakerSizeUpdate


async def send_update_sneaker_sizes_data(
    producer,
    sneaker_id: int,
    sneaker_size_update: SneakerSizeUpdate,
):
    sneaker_sizes_update_payload = {
        "event_type": "sneaker_sizes_updated",
        "data": sneaker_size_update.dict(),
    }
    await producer.send_and_wait(
        settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_update_payload,
    )
