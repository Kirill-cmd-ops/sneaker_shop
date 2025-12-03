from sqlalchemy.ext.asyncio import AsyncSession
from stock_notification_service.stock_notification.models import db_helper
from stock_notification_service.stock_notification.seeds.seed_brands import seed_brands
from stock_notification_service.stock_notification.seeds.seed_sizes import seed_sizes
from stock_notification_service.stock_notification.seeds.seed_sneakers import (
    seed_sneakers,
)
from stock_notification_service.stock_notification.seeds.seed_users import seed_users


async def run_seeds():
    session_gen = db_helper.session_getter()
    session: AsyncSession = await anext(session_gen)

    try:
        await seed_brands(session)
        await seed_sizes(session)
        await seed_sneakers(session)
        await seed_users(session)
        await session.commit()
        print("All seeds completed successfully!")
    except Exception as e:
        await session.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        await session.close()
