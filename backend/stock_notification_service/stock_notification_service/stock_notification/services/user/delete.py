from sqlalchemy import delete

from stock_notification_service.stock_notification.models import User, db_helper


async def delete_user_service(user_id: int):
    async with db_helper.session_context() as session:
        async with session.begin():
            stmt = delete(User).where(User.id == user_id)
            await session.execute(stmt)
