from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.config import settings


async def publish_sneaker_viewed(
        producer,
        sneaker_id: int,
        user_id: int,
):
    payload = {"user_id": user_id, "sneaker_id": sneaker_id}

    await producer.send_and_wait(
        topic=settings.kafka_config.sneaker_viewed_topic,
        key=str(user_id),
        value=payload,
    )
