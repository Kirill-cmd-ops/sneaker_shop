from fastapi.encoders import jsonable_encoder

from auth_service.auth.config import settings
from auth_service.auth.schemas import UserCreate, UserUpdate


async def publish_user_created(
    producer,
    user_id: int,
    user_create: UserCreate,
):
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
    producer,
    user_id: int,
    user_update: UserUpdate,
):
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


async def publish_user_deleted(producer, user_id: int):
    user_delete_payload = {"event_type": "user_deleted", "user_id": user_id}

    await producer.send_and_wait(
        topic=settings.kafka_config.user_work_topic,
        key=str(user_id),
        value=user_delete_payload,
    )
