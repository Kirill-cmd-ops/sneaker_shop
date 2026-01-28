from aiokafka import AIOKafkaProducer
from fastapi import Request


async def get_kafka_producer(request: Request) -> AIOKafkaProducer:
    return request.app.state.kafka_producer
