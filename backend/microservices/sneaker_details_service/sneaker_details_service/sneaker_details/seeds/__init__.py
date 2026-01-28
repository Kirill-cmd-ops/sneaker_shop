from sqlalchemy.ext.asyncio import AsyncSession
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.models import db_helper
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.brands import seed_brands
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.sizes import seed_sizes
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.sneakers import seed_sneakers
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.sneaker_sizes import (
    seed_sneaker_sizes,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.countries import seed_countries
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.colors import seed_colors
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.sneaker_colors import (
    seed_sneaker_colors,
)
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.materials import seed_materials
from microservices.sneaker_details_service.sneaker_details_service.sneaker_details.seeds.sneaker_materials import (
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
