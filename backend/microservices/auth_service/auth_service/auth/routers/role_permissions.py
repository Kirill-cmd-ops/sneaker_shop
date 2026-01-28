from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from microservices.auth_service.auth_service.auth.config import settings
from microservices.auth_service.auth_service.auth.models import db_helper
from microservices.auth_service.auth_service.auth.schemas.permissions import UpdatePermissions
from microservices.auth_service.auth_service.auth.dependencies.permissions import check_role_permissions
from microservices.auth_service.auth_service.auth.services.role_permission.orchestrators import (
    update_role_permissions_orchestrator,
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
async def update_role_permissions(
        request: Request,
        update_permissions: UpdatePermissions,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    user_role = request.state.user_role
    redis_client = request.state.redis_client

    list_permissions = update_permissions.list_permission

    return await update_role_permissions_orchestrator(
        session=session,
        redis_client=redis_client,
        user_role=user_role,
        list_permissions=list_permissions,
    )
