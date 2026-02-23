from aiokafka import AIOKafkaProducer
from fastapi.encoders import jsonable_encoder

from microservices.auth_service.auth_service.auth.config import settings
from microservices.auth_service.auth_service.auth.schemas import UserCreate, UserUpdate


async def publish_user_created(
        producer: AIOKafkaProducer,
        user_id: int,
        user_create: UserCreate,
) -> None:
    user_create_payload = {
        "event_type": "user_created",
        "data": user_create.dict(
            exclude={"password", "confirm_password"},
        ),
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.user_work_topic,
        key=str(user_id),
        value=jsonable_encoder(user_create_payload),
    )


async def publish_user_updated(
        producer: AIOKafkaProducer,
        user_id: int,
        user_update: UserUpdate,
) -> None:
    user_update_payload = {
        "event_type": "user_updated",
        "user_id": user_id,
        "data": user_update.dict(
            exclude_unset=True,
            exclude={"password"},
        ),
    }

    await producer.send_and_wait(
        topic=settings.kafka_config.user_work_topic,
        key=str(user_id),
        value=jsonable_encoder(user_update_payload),
    )


async def publish_user_deleted(
        producer: AIOKafkaProducer,
        user_id: int
) -> None:
    user_delete_payload = {"event_type": "user_deleted", "user_id": user_id}

    await producer.send_and_wait(
        topic=settings.kafka_config.user_work_topic,
        key=str(user_id),
        value=user_delete_payload,
    )
