import json

from aiokafka import AIOKafkaProducer
from fastapi.encoders import jsonable_encoder

from auth_service.auth.config import settings
from sneaker_details_service.sneaker_details.schemas import SneakerCreate, SneakerUpdate


# TODO: разобраться с импортом, так как создание тут функций это временное решение


async def start_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_config.kafka_bootstrap_servers,
        key_serializer=lambda d: d.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    await producer.start()
    return producer


async def close_producer(producer):
    await producer.stop()


async def send_user_registered(producer, user_id: str):
    payload = {"id": user_id}
    await producer.send_and_wait(
        settings.kafka_config.registered_topic, key=user_id, value=payload
    )


async def send_create_sneaker_data(
    producer,
    sneaker_id: int,
    sneaker_create: SneakerCreate,
):
    sneaker_create_payload = {
        "event_type": "sneaker_created",
        "data": sneaker_create.dict(
            exclude={"description", "country_id", "color_ids", "material_ids"}
        ),
    }

    await producer.send_and_wait(
        settings.kafka_config.sneaker_topic,
        key=str(sneaker_id),
        value=jsonable_encoder(sneaker_create_payload),
    )


async def send_delete_sneaker_data(producer, sneaker_id: int):
    sneaker_delete_payload = {"event_type": "sneaker_deleted", "sneaker_id": sneaker_id}

    await producer.send_and_wait(
        settings.kafka_config.sneaker_topic,
        key=str(sneaker_id),
        value=sneaker_delete_payload,
    )


async def send_update_sneaker_data(
    producer,
    sneaker_id: int,
    sneaker_update: SneakerUpdate,
):
    sneaker_update_payload = {
        "event_type": "sneaker_updated",
        "data": sneaker_update.dict(
            exclude={"description", "country_id"}
        ),
    }

    await producer.send_and_wait(
        settings.kafka_config.sneaker_topic,
        key=str(sneaker_id),
        value=jsonable_encoder(sneaker_update_payload),
    )
