from favorite_service.favorite.models import db_helper, Size
from favorite_service.favorite.schemas import SizeCreate
from favorite_service.favorite.services.record.create import create_record
from favorite_service.favorite.services.record.delete import delete_record


async def handle_size(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "size_created":
                data = value.get("data")
                size_create = SizeCreate(**data)
                await create_record(
                    session=session,
                    table_name=Size,
                    schema_create=size_create,
                )

            elif event_type == "size_deleted":
                size_id = value.get("size_id")
                await delete_record(
                    session=session,
                    table_name=Size,
                    record_id=size_id,
                )
    except Exception as e:
        print("Ошибка:", e)
