from microservices.stock_notification_service.stock_notification_service.stock_notification.models import db_helper
from microservices.stock_notification_service.stock_notification_service.stock_notification.seeds.brands import \
    seed_brands
from microservices.stock_notification_service.stock_notification_service.stock_notification.seeds.sizes import \
    seed_sizes
from microservices.stock_notification_service.stock_notification_service.stock_notification.seeds.sneaker_sizes import (
    seed_sneaker_sizes,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.seeds.sneakers import (
    seed_sneakers,
)
from microservices.stock_notification_service.stock_notification_service.stock_notification.seeds.users import \
    seed_users


async def run_seeds():
    async with db_helper.session_getter() as session:
        async with session.begin():
            await seed_brands(session=session)
            await seed_sizes(session=session)
            await seed_sneakers(session=session)
            await seed_sneaker_sizes(session=session)
            await seed_users(session=session)

    print("All seeds completed successfully!")
