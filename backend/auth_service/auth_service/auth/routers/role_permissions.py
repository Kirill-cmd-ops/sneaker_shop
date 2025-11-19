from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from auth_service.auth.config import settings
from auth_service.auth.models import db_helper, Permission
from auth_service.auth.schemas.permissions import UpdatePermissions
from auth_service.auth.dependencies.check_permissions import check_role_permissions
from auth_service.auth.services.role_permissions import update_role_permissions

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.role_permissions,
    )
)


@router.put(
    "/update",
    dependencies=(Depends(check_role_permissions("favorite.view")),),
)
async def call_update_role_permissions(
    request: Request,
    update_permissions: UpdatePermissions,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    redis_client = request.state.redis_client
    user_role = request.state.user_role

    if update_permissions.list_permission:
        await update_role_permissions(
            user_role=user_role,
            list_permission=update_permissions.list_permission,
            session=session,
        )

        stmt = select(Permission.name).where(
            Permission.id.in_(update_permissions.list_permission)
        )
        result = await session.execute(stmt)
        name_permissions = [permission[0] for permission in result.all()]

        async with redis_client.pipeline() as pipe:
            await pipe.delete(f"role:{user_role}")
            if name_permissions:
                await pipe.sadd(f"role:{user_role}", *name_permissions)
                await pipe.execute()

    return {"status": "ok"}
