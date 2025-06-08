from sqlalchemy.ext.asyncio import AsyncSession
from catalog_service.catalog.models.db_helper import db_helper
from catalog_service.catalog.seeds.seed_brands import seed_brands
from catalog_service.catalog.seeds.seed_sizes import seed_sizes
from catalog_service.catalog.seeds.seed_sneakers import seed_sneakers
from catalog_service.catalog.seeds.seed_sneaker_sizes import seed_sneaker_sizes

async def run_seeds():
    session_gen = db_helper.session_getter()
    session: AsyncSession = await anext(session_gen)

    try:
        await seed_brands(session)
        await seed_sizes(session)
        await seed_sneakers(session)
        await seed_sneaker_sizes(session)
        await session.commit()
        print("All seeds completed successfully!")
    except Exception as e:
        await session.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        await session.close()

