from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from stock_notification_service.stock_notification.models import User


async def seed_users(session: AsyncSession):
    users = [
        {"email": "bondarenkokirill150208@gmail.com"},
        {"email": "pubginvolker@gmail.com"},
        {"email": "snulat90@gmail.com"},
        {"email": "bondarenko15022008@gmail.com"},
        {"email": "eenn45895@gmail.com"},
        {"email": "ki15022008@gmail.com"},
    ]
    stmt = insert(User).values(users)
    await session.execute(stmt)
    await session.commit()
