from auth_service.auth.config import settings


async def send_user_registered(producer, user_id: str):
    payload = {"id": user_id}
    await producer.send_and_wait(
        settings.kafka_config.registered_topic, key=user_id, value=payload
    )