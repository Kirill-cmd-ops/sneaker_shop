from fastapi.encoders import jsonable_encoder

from auth_service.auth.config import settings
from auth_service.auth.schemas import UserCreate


async def send_create_user_data(
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
