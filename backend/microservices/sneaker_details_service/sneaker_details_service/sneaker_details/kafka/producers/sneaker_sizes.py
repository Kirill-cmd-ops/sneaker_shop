from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.schemas import (
    SneakerSizesCreate,
    SneakerAssocsDelete,
    SneakerSizeUpdate,
)


async def publish_sneaker_sizes_created(
        producer,
        sneaker_id: int,
        sneaker_sizes_create: SneakerSizesCreate,
):
    sneaker_sizes_create_payload = {
        "event_type": "sneaker_sizes_created",
        "data": sneaker_sizes_create.dict(),
    }
    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_create_payload,
    )


async def publish_sneaker_size_updated(
        producer,
        sneaker_id: int,
        sneaker_size_update: SneakerSizeUpdate,
):
    sneaker_sizes_update_payload = {
        "event_type": "sneaker_sizes_updated",
        "data": sneaker_size_update.dict(),
    }
    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_update_payload,
    )


async def publish_sneaker_sizes_deleted(
        producer,
        sneaker_id: int,
        sneaker_sizes_delete: SneakerAssocsDelete,
):
    sneaker_sizes_delete_payload = {
        "event_type": "sneaker_sizes_deleted",
        "data": sneaker_sizes_delete.dict(),
    }
    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_delete_payload,
    )
