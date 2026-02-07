from microservices.favorite_service.favorite_service.favorite.models.db_helper import db_helper
from microservices.favorite_service.favorite_service.favorite.seeds.brands import seed_brands
from microservices.favorite_service.favorite_service.favorite.seeds.sizes import seed_sizes
from microservices.favorite_service.favorite_service.favorite.seeds.sneakers import seed_sneakers
from microservices.favorite_service.favorite_service.favorite.seeds.sneaker_sizes import seed_sneaker_sizes


async def run_seeds():
    async with db_helper.session_getter() as session:
        async with session.begin():
            await seed_brands(session=session)
            await seed_sizes(session=session)
            await seed_sneakers(session=session)
            await seed_sneaker_sizes(session=session)

    print("All seeds completed successfully!")
