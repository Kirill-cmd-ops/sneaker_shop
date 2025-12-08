from stock_notification_service.stock_notification.models import db_helper, Brand
from stock_notification_service.stock_notification.schemas import BrandCreate
from stock_notification_service.stock_notification.services.record import create_record, delete_record



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
