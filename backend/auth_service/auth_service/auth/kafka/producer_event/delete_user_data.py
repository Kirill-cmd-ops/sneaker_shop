from auth_service.auth.config import settings


async def send_delete_user_data(producer, user_id: int):
    user_delete_payload = {"event_type": "user_deleted", "user_id": user_id}

    await producer.send_and_wait(
        topic=settings.kafka_config.user_work_topic,
        key=str(user_id),
        value=user_delete_payload,
    )