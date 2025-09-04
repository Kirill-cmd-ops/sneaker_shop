from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import db_helper
from auth_service.auth.seeds.seed_roles import seed_roles


async def run_seeds():
    session_gen = db_helper.session_getter()
    session: AsyncSession = await anext(session_gen)

    try:
        await seed_roles(session)
        await session.commit()
        print("All seeds completed successfully!")
    except Exception as e:
        await session.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        await session.close()