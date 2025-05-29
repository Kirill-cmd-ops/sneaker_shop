from sqlalchemy.ext.asyncio import AsyncSession
from backend.auth_servicee import db_helper
from backend.core.seeds.seed_brands import seed_brands
from backend.core.seeds.seed_sizes import seed_sizes
from backend.core.seeds.seed_sneakers import seed_sneakers
from backend.core.seeds.seed_sneaker_sizes import seed_sneaker_sizes
from backend.core.seeds.seed_countries import seed_countries
from backend.core.seeds.seed_colors import seed_colors
from backend.core.seeds.seed_sneaker_colors import seed_sneaker_colors
from backend.core.seeds.seed_materials import seed_materials
from backend.core.seeds.seed_sneaker_materials import seed_sneaker_materials

async def run_seeds():
    session_gen = db_helper.session_getter()
    session: AsyncSession = await anext(session_gen)

    try:
        await seed_brands(session)
        await seed_sizes(session)
        await seed_countries(session)
        await seed_sneakers(session)
        await seed_sneaker_sizes(session)
        await seed_colors(session)
        await seed_sneaker_colors(session)
        await seed_materials(session)
        await seed_sneaker_materials(session)
        await session.commit()
        print("All seeds completed successfully!")
    except Exception as e:
        await session.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        await session.close()

