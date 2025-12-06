from sneaker_details_service.sneaker_details.config import settings


async def send_delete_size_data(producer, size_id: int):
    size_delete_payload = {"event_type": "size_deleted", "size_id": size_id}

    await producer.send_and_wait(
        settings.kafka_config.size_work_topic,
        key=str(size_id),
        value=size_delete_payload,
    )