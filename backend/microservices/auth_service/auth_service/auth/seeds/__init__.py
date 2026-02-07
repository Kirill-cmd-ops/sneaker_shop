from microservices.auth_service.auth_service.auth.models import db_helper
from microservices.auth_service.auth_service.auth.seeds.roles import seed_roles
from microservices.auth_service.auth_service.auth.seeds.permissions import seed_permission


async def run_seeds():
    async with db_helper.session_getter() as session:
        async with session.begin():
            await seed_roles(session=session)
            await seed_permission(session=session)

    print("All seeds completed successfully!")
