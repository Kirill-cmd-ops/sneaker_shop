from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import Role, RolePermissionAssociation, Permission
from auth_service.auth.schemas.permissions import UpdatePermissions


async def update_role_permissions(
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



async def get_role_permissions(
    session: AsyncSession,
    update_permissions: UpdatePermissions,
):
    stmt = select(Permission.name).where(
        Permission.id.in_(update_permissions.list_permission)
    )
    result = await session.execute(stmt)
    return result
