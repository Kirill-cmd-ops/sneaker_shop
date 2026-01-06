from favorite_service.favorite.models import db_helper, Brand
from favorite_service.favorite.schemas import BrandCreate
from favorite_service.favorite.services.record.create import create_record
from favorite_service.favorite.services.record.delete import delete_record


async def handle_brand(key: str | None, value: dict):
    try:
        event_type = value.get("event_type")
        async with db_helper.session_context() as session:
            if event_type == "brand_created":
                data = value.get("data")
                brand_create = BrandCreate(**data)
                await create_record(session, Brand, brand_create)

            elif event_type == "brand_deleted":
                brand_id = value.get("brand_id")
                await delete_record(session, Brand, brand_id)
    except Exception as e:
        print("Ошибка:", e)
