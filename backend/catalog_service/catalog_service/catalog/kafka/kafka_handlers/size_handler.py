from catalog_service.catalog.models import db_helper, Size
from catalog_service.catalog.schemas import SizeCreate
from catalog_service.catalog.services.record.create import create_record
from catalog_service.catalog.services.record.delete import delete_record


async def handle_size(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "size_created":
                data = value.get("data")
                size_create = SizeCreate(**data)
                await create_record(session, Size, size_create)

            elif event_type == "size_deleted":
                size_id = value.get("size_id")
                await delete_record(session, Size, size_id)
    except Exception as e:
        print("Ошибка:", e)
