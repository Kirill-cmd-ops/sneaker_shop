from sqlalchemy.ext.asyncio import AsyncSession
from stock_notification_service.stock_notification.models import User

async def seed_users(db: AsyncSession):
    users = [
        User(email="bondarenkokirill150208@gmail.com"),
        User(email="pubginvolker@gmail.com"),
        User(email="snulat90@gmail.com"),
        User(email="bondarenko15022008@gmail.com"),
        User(email="eenn45895@gmail.com"),
        User(email="ki15022008@gmail.com"),
    ]
    db.add_all(users)
    await db.flush()
    await db.commit()
