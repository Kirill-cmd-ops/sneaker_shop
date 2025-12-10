from starlette.requests import Request


async def update_role_permissions(redis_client, user_role: str, list_role_permissions: list[str]):

    async with redis_client.pipeline() as pipe:
        await pipe.delete(f"role:{user_role}")
        if list_role_permissions:
            await pipe.sadd(f"role:{user_role}", *list_role_permissions)
            await pipe.execute()
