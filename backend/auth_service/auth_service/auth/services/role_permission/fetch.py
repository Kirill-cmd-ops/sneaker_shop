from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import Permission
from auth_service.auth.schemas.permissions import UpdatePermissions


async def get_role_permissions_db(
    session: AsyncSession,
    update_permissions: UpdatePermissions,
):
    result = await session.scalars(
        select(Permission.name).where(
            Permission.id.in_(update_permissions.list_permission)
        ),
    )
    return result.all()
