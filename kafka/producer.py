import os
import json

from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv

load_dotenv()
BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
REGISTERED_TOPIC = os.getenv("REGISTERED_TOPIC")


producer = AIOKafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    key_serializer=lambda d: d.encode("utf-8"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


async def start_producer():
    await producer.start()

async def close_producer():
    await producer.stop()

async def send_user_registered(user_id: str):
    payload = {"id": user_id}
    await producer.send_and_wait(
        REGISTERED_TOPIC,
        key=user_id,
        value=payload
    )

