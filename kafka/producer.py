import json

from aiokafka import AIOKafkaProducer


async def start_producer(bootstrap_servers):
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        key_serializer=lambda d: d.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    await producer.start()
    return producer


async def close_producer(producer):
    await producer.stop()
