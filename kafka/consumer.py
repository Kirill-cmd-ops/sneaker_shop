import json
import os

from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv


load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
REGISTERED_TOPIC = os.getenv("REGISTERED_TOPIC")
CART_GROUP_ID = os.getenv("CART_GROUP_ID")
FAVORITE_GROUP_ID = os.getenv("FAVORITE_GROUP_ID")


def create_consumer(
    topic: str, bootstrap_servers: str, group_id: str
) -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
    )


cart_consumer = create_consumer(
    REGISTERED_TOPIC,
    group_id=CART_GROUP_ID,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
)

favorite_consumer = create_consumer(
    REGISTERED_TOPIC,
    group_id=FAVORITE_GROUP_ID,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
)
