from fastapi.encoders import jsonable_encoder

from auth_service.auth.config import settings
from auth_service.auth.schemas import UserUpdate


async def send_update_user_data(
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
        settings.kafka_config.user_work_topic,
        key=str(user_id),
        value=jsonable_encoder(user_update_payload),
    )
