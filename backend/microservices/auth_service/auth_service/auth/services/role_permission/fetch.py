from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.auth.models import Permission


async def get_role_permissions_db(
    session: AsyncSession,
    list_permissions: list[int],
):
    result = await session.scalars(
        select(Permission.name).where(Permission.id.in_(list_permissions)),
    )
    return result.all()
