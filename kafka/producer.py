import json

from aiokafka import AIOKafkaProducer


async def start_producer(bootstrap_servers):
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        key_serializer=lambda d: d.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        enable_idempotence=True,
        retry_backoff_ms=200,
        request_timeout_ms=30000,
        linger_ms=20,
        max_batch_size=65536,
        compression_type="lz4"
    )
    await producer.start()
    return producer


async def close_producer(producer):
    await producer.stop()
