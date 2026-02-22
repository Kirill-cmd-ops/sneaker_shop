from typing import Dict, Any

from aiokafka import AIOKafkaProducer
from fastapi.encoders import jsonable_encoder

from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings


async def publish_size_created(
        producer: AIOKafkaProducer,
        size_id: int,
        size_data: Dict[str, Any],
) -> None:
    size_create_payload = {
        "event_type": "size_created",
        "data": size_data,
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.size_work_topic,
        key=str(size_id),
        value=jsonable_encoder(size_create_payload),
    )


async def publish_size_deleted(
        producer: AIOKafkaProducer,
        size_id: int,
) -> None:
    size_delete_payload = {
        "event_type": "size_deleted",
        "size_id": size_id,
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.size_work_topic,
        key=str(size_id),
        value=size_delete_payload,
    )
