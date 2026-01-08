from sneaker_details_service.sneaker_details.config import settings


async def send_delete_sneaker_data(producer, sneaker_id: int):
    sneaker_delete_payload = {"event_type": "sneaker_deleted", "sneaker_id": sneaker_id}

    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_work_topic,
        key=str(sneaker_id),
        value=sneaker_delete_payload,
    )
