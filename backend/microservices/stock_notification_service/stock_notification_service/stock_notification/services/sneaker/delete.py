from sqlalchemy import delete

from stock_notification_service.stock_notification.models import Sneaker, db_helper


async def delete_sneaker_service(sneaker_id: int):
    async with db_helper.session_context() as session:
        async with session.begin():
            stmt = delete(Sneaker).where(Sneaker.id == sneaker_id)
            await session.execute(stmt)
