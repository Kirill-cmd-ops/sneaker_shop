from stock_notification_service.stock_notification.models import User, db_helper
from stock_notification_service.stock_notification.schemas import UserCreate


async def create_user_service(
    user_create: UserCreate,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            user = User(**user_create.dict())
            session.add(user)
