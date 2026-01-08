from sqlalchemy.ext.asyncio import AsyncSession
from sneaker_details_service.sneaker_details.models import db_helper
from sneaker_details_service.sneaker_details.seeds.seed_brands import seed_brands
from sneaker_details_service.sneaker_details.seeds.seed_sizes import seed_sizes
from sneaker_details_service.sneaker_details.seeds.seed_sneakers import seed_sneakers
from sneaker_details_service.sneaker_details.seeds.seed_sneaker_sizes import (
    seed_sneaker_sizes,
)
from sneaker_details_service.sneaker_details.seeds.seed_countries import seed_countries
from sneaker_details_service.sneaker_details.seeds.seed_colors import seed_colors
from sneaker_details_service.sneaker_details.seeds.seed_sneaker_colors import (
    seed_sneaker_colors,
)
from sneaker_details_service.sneaker_details.seeds.seed_materials import seed_materials
from sneaker_details_service.sneaker_details.seeds.seed_sneaker_materials import (
    seed_sneaker_materials,
)


async def run_seeds():
    session_gen = db_helper.session_getter()
    session: AsyncSession = await anext(session_gen)

    try:
        await seed_brands(session=session)
        await seed_sizes(session=session)
        await seed_countries(session=session)
        await seed_sneakers(session=session)
        await seed_sneaker_sizes(session=session)
        await seed_colors(session=session)
        await seed_sneaker_colors(session=session)
        await seed_materials(session=session)
        await seed_sneaker_materials(session=session)
        await session.commit()
        print("All seeds completed successfully!")
    except Exception as e:
        await session.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        await session.close()
