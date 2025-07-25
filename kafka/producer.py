import json

from aiokafka import AIOKafkaProducer

from auth_service.auth.config import settings


async def start_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        key_serializer=lambda d: d.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    return producer

async def close_producer(producer):
    await producer.stop()

async def send_user_registered(producer, user_id: str):
    payload = {"id": user_id}
    await producer.send_and_wait(
        settings.kafka_config.registered_topic,
        key=user_id,
        value=payload
    )

