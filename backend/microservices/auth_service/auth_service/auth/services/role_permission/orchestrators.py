from sqlalchemy.ext.asyncio import AsyncSession

from microservices.auth_service.auth_service.auth.services.role_permission.fetch import get_role_permissions_db
from microservices.auth_service.auth_service.auth.services.role_permission.update import update_role_permissions_db, \
    update_role_permissions_redis

import redis.asyncio as aioredis


async def update_role_permissions_orchestrator(
        session: AsyncSession,
        redis_client: aioredis.Redis,
        user_role: str,
        list_permissions: list[int],
):
    async with session.begin():
        if list_permissions:
            await update_role_permissions_db(
                user_role=user_role,
                list_permissions=list_permissions,
                session=session,
            )

            role_permissions = await get_role_permissions_db(
                session=session,
                list_permissions=list_permissions,
            )

    list_role_permissions = [permission[0] for permission in role_permissions]
    if list_role_permissions is not None:
        await update_role_permissions_redis(
            redis_client=redis_client,
            user_role=user_role,
            list_role_permissions=list_role_permissions,
        )

    return {"status": "ok"}
