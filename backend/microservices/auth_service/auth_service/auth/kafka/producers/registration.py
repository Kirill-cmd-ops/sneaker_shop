from aiokafka import AIOKafkaProducer

from microservices.auth_service.auth_service.auth.config import settings


async def publish_user_registered(
        producer: AIOKafkaProducer,
        user_id: str
) -> None:
    payload = {"id": user_id}
    await producer.send_and_wait(
        topic=settings.kafka_config.registered_topic,
        key=user_id,
        value=payload,
    )
