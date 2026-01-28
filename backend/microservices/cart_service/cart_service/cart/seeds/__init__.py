from sqlalchemy.ext.asyncio import AsyncSession
from microservices.cart_service.cart_service.cart.models.db_helper import db_helper
from microservices.cart_service.cart_service.cart.seeds.brands import seed_brands
from microservices.cart_service.cart_service.cart.seeds.sizes import seed_sizes
from microservices.cart_service.cart_service.cart.seeds.sneakers import seed_sneakers
from microservices.cart_service.cart_service.cart.seeds.sneaker_sizes import seed_sneaker_sizes


async def run_seeds():
    session_gen = db_helper.session_getter()
    session: AsyncSession = await anext(session_gen)

    try:
        await seed_brands(session=session)
        await seed_sizes(session=session)
        await seed_sneakers(session=session)
        await seed_sneaker_sizes(session=session)
        await session.commit()
        print("All seeds completed successfully!")
    except Exception as e:
        await session.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        await session.close()
