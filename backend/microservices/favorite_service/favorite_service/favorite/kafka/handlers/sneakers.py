from microservices.favorite_service.favorite_service.favorite.schemas import SneakerCreate, SneakerUpdate
from microservices.favorite_service.favorite_service.favorite.services.sneaker.create import create_sneaker_service
from microservices.favorite_service.favorite_service.favorite.services.sneaker.delete import delete_sneaker_service
from microservices.favorite_service.favorite_service.favorite.services.sneaker.update import update_sneaker_service


async def handle_sneaker_event(key: str | None, value: dict) -> None:
    event_type = value.get("event_type")
    if event_type == "sneaker_created":
        data = value.get("data")
        sneaker_create = SneakerCreate(**data)
        sneaker_create_data = sneaker_create.model_dump(exclude={"size_ids"})
        size_ids = [
            size.model_dump(include={"size_id", "quantity"})
            for size in sneaker_create.size_ids
        ]

        await create_sneaker_service(
            sneaker_data=sneaker_create_data,
            size_ids=size_ids,
        )
    elif event_type == "sneaker_updated":
        data = value.get("data")
        sneaker_id = value.get("sneaker_id")
        sneaker_update = SneakerUpdate(**data)
        sneaker_update_data = sneaker_update.model_dump(exclude_unset=True)
        await update_sneaker_service(
            sneaker_id=sneaker_id,
            sneaker_data=sneaker_update_data,
        )

    elif event_type == "sneaker_deleted":
        sneaker_id = value.get("sneaker_id")
        await delete_sneaker_service(sneaker_id=sneaker_id)
