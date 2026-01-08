from sneaker_details_service.sneaker_details.config import settings


async def send_delete_brand_data(producer, brand_id: int):
    brand_delete_payload = {"event_type": "brand_deleted", "brand_id": brand_id}

    await producer.send_and_wait(
        topic=settings.kafka_config.brand_work_topic,
        key=str(brand_id),
        value=brand_delete_payload,
    )
