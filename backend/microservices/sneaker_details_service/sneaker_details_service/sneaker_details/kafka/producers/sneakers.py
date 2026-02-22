from typing import Dict, Any

from aiokafka import AIOKafkaProducer
from fastapi.encoders import jsonable_encoder

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings


async def publish_sneaker_created(
        producer: AIOKafkaProducer,
        sneaker_id: int,
        sneaker_data: Dict[str, Any],
) -> None:
    sneaker_create_payload = {
        "event_type": "sneaker_created",
        "data": sneaker_data,
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_work_topic,
        key=str(sneaker_id),
        value=jsonable_encoder(sneaker_create_payload),
    )


async def publish_sneaker_updated(
        producer: AIOKafkaProducer,
        sneaker_id: int,
        sneaker_data: Dict[str, Any],
) -> None:
    sneaker_update_payload = {
        "event_type": "sneaker_updated",
        "sneaker_id": sneaker_id,
        "data": sneaker_data,
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_work_topic,
        key=str(sneaker_id),
        value=jsonable_encoder(sneaker_update_payload),
    )


async def publish_sneaker_deleted(
        producer: AIOKafkaProducer,
        sneaker_id: int,
) -> None:
    sneaker_delete_payload = {
        "event_type": "sneaker_deleted",
        "sneaker_id": sneaker_id,
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_work_topic,
        key=str(sneaker_id),
        value=sneaker_delete_payload,
    )
