from typing import Dict, Any

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings


async def publish_sneaker_sizes_created(
        producer,
        sneaker_id: int,
        sneaker_sizes_data: Dict[str, Any],
):
    sneaker_sizes_create_payload = {
        "event_type": "sneaker_sizes_created",
        "data": sneaker_sizes_data,
    }
    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_create_payload,
    )


async def publish_sneaker_size_updated(
        producer,
        sneaker_id: int,
        size_id: int,
        quantity: int,
):
    sneaker_sizes_update_payload = {
        "event_type": "sneaker_sizes_updated",
        "data": {"size_id": size_id, "quantity": quantity},
    }
    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_update_payload,
    )


async def publish_sneaker_sizes_deleted(
        producer,
        sneaker_id: int,
        size_ids: list[int],
):
    sneaker_sizes_delete_payload = {
        "event_type": "sneaker_sizes_deleted",
        "data": {"assoc_ids": size_ids},
    }
    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_sizes_work_topic,
        key=str(sneaker_id),
        value=sneaker_sizes_delete_payload,
    )
