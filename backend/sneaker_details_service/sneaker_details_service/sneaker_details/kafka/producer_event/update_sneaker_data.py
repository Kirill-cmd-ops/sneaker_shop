from fastapi.encoders import jsonable_encoder

from sneaker_details_service.sneaker_details.config import settings
from sneaker_details_service.sneaker_details.schemas import SneakerUpdate


async def send_update_sneaker_data(
    producer,
    sneaker_id: int,
    sneaker_update: SneakerUpdate,
):
    sneaker_update_payload = {
        "event_type": "sneaker_updated",
        "data": sneaker_update.dict(exclude={"description", "country_id"}),
    }

    await producer.send_and_wait(
        settings.kafka_config.sneaker_work_topic,
        key=str(sneaker_id),
        value=jsonable_encoder(sneaker_update_payload),
    )