from microservices.catalog_service.catalog_service.catalog.models import db_helper, Size
from microservices.catalog_service.catalog_service.catalog.schemas import SizeCreate
from microservices.catalog_service.catalog_service.catalog.services.record.create import create_record_service
from microservices.catalog_service.catalog_service.catalog.services.record.delete import delete_record_service


async def handle_size_event(key: str | None, value: dict) -> None:
    event_type = value.get("event_type")
    if event_type == "size_created":
        data = value.get("data")
        size_create = SizeCreate(**data)
        size_create_data = size_create.model_dump()
        await create_record_service(
            table_name=Size,
            data=size_create_data,
        )

    elif event_type == "size_deleted":
        size_id = value.get("size_id")
        await delete_record_service(
            table_name=Size,
            record_id=size_id,
        )
