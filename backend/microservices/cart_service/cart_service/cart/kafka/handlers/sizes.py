from microservices.cart_service.cart_service.cart.models import Size
from microservices.cart_service.cart_service.cart.schemas import SizeCreate
from microservices.cart_service.cart_service.cart.services.record.create import create_record_service
from microservices.cart_service.cart_service.cart.services.record.delete import delete_record_service


async def handle_size_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        if event_type == "size_created":
            data = value.get("data")
            size_create = SizeCreate(**data)
            await create_record_service(
                table_name=Size,
                schema_create=size_create,
            )

        elif event_type == "size_deleted":
            size_id = value.get("size_id")
            await delete_record_service(
                table_name=Size,
                record_id=size_id,
            )
    except Exception as e:
        print("Ошибка:", e)
