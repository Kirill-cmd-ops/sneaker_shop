from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from auth_service.auth.config import settings
from auth_service.auth.models import db_helper
from auth_service.auth.schemas.permissions import UpdatePermissions
from auth_service.auth.dependencies.check_permissions import check_role_permissions
from auth_service.auth.services.role_permission.update import update_role_permissions_db
from auth_service.auth.services.role_permission.fetch import get_role_permissions_db


from auth_service.auth.services.role_permission.update import (
    update_role_permissions_redis,
)

router = APIRouter(
    prefix=settings.api.build_path(
        settings.api.root,
        settings.api.v1.prefix,
        settings.api.v1.role_permissions,
    ),
    tags=["Role Permissions"],
)


@router.put(
    "/",
    dependencies=(Depends(check_role_permissions("favorite.view")),),
)
async def call_update_role_permissions(
    request: Request,
    update_permissions: UpdatePermissions,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    user_role = request.state.user_role
    redis_client = request.state.redis_client

    async with session.begin():
        if update_permissions.list_permission:
            await update_role_permissions_db(
                user_role=user_role,
                list_permission=update_permissions.list_permission,
                session=session,
            )

            role_permissions = await get_role_permissions_db(
                session=session,
                update_permissions=update_permissions,
            )

    list_role_permissions = [permission[0] for permission in role_permissions]
    if list_role_permissions is not None:
        await update_role_permissions_redis(
            redis_client=redis_client,
            user_role=user_role,
            list_role_permissions=list_role_permissions,
        )

    return {"status": "ok"}
