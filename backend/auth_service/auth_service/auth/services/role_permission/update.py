from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import Role, RolePermissionAssociation


async def update_role_permissions_db(
    user_role: str,
    list_permission: list[int],
    session: AsyncSession,
):
    role_id = await session.scalar(select(Role.id).where(Role.name == user_role))

    if not role_id:
        raise HTTPException(status_code=404, detail="Role id not found")

    stmt = select(RolePermissionAssociation.permission_id).where(
        RolePermissionAssociation.role_id == role_id
    )
    result = await session.execute(stmt)
    permissions = set(result.scalars())

    new_permissions = set(list_permission)

    for perm in new_permissions - permissions:
        session.add(RolePermissionAssociation(role_id=role_id, permission_id=perm))

    remove_permissions = permissions - new_permissions
    await session.execute(
        delete(RolePermissionAssociation).where(
            RolePermissionAssociation.role_id == role_id,
            RolePermissionAssociation.permission_id.in_(remove_permissions),
        )
    )


async def update_role_permissions_redis(redis_client, user_role: str, list_role_permissions: list[str]):

    async with redis_client.pipeline() as pipe:
        await pipe.delete(f"role:{user_role}")
        if list_role_permissions:
            await pipe.sadd(f"role:{user_role}", *list_role_permissions)
            await pipe.execute()