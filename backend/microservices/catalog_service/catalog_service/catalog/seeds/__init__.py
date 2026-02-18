from microservices.catalog_service.catalog_service.catalog.models.db_helper import db_helper
from microservices.catalog_service.catalog_service.catalog.seeds.brands import seed_brands
from microservices.catalog_service.catalog_service.catalog.seeds.sizes import seed_sizes
from microservices.catalog_service.catalog_service.catalog.seeds.sneakers import seed_sneakers
from microservices.catalog_service.catalog_service.catalog.seeds.sneaker_sizes import seed_sneaker_sizes


async def run_seeds() -> None:
    async with db_helper.session_getter() as session:
        async with session.begin():
            await seed_brands(session=session)
            await seed_sizes(session=session)
            await seed_sneakers(session=session)
            await seed_sneaker_sizes(session=session)

    print("All seeds completed successfully!")
