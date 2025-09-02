from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import SneakerAssocsDelete


async def send_delete_sneaker_sizes_data(
    producer,
    sneaker_sizes_delete: SneakerAssocsDelete,
):
    sneaker_sizes_delete_payload = {
        "event_type": "sneaker_sizes_deleted",
        "data": sneaker_sizes_delete.dict(),
    }
    await producer.send_and_wait(
        settings.kafka_config.sneaker_topic,
        key=str(sneaker_sizes_delete.sneaker_id),
        value=sneaker_sizes_delete_payload,
    )