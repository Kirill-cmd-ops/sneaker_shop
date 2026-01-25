from catalog_service.catalog.models import db_helper, Brand
from catalog_service.catalog.schemas import BrandCreate
from catalog_service.catalog.services.record.create import create_record_service
from catalog_service.catalog.services.record.delete import delete_record_service


async def handle_brand_event(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        if event_type == "brand_created":
            data = value.get("data")
            brand_create = BrandCreate(**data)
            await create_record_service(
                table_name=Brand,
                schema_create=brand_create,
            )

        elif event_type == "brand_deleted":
            brand_id = value.get("brand_id")
            await delete_record_service(
                table_name=Brand,
                record_id=brand_id,
            )
    except Exception as e:
        print("Ошибка:", e)
