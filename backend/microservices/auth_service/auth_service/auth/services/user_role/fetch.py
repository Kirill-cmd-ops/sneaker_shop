from fastapi import HTTPException
from sqlalchemy import select

from microservices.auth_service.auth_service.auth.models import db_helper, Role, UserRoleAssociation


async def get_user_role(user_id: int):
    async with db_helper.session_context() as session:
        role = await session.scalar(
            select(Role.name)
            .join(UserRoleAssociation, Role.id == UserRoleAssociation.role_id)
            .where(UserRoleAssociation.user_id == user_id))

        if not role:
            raise HTTPException(
                status_code=404, detail="У данного пользователя нету role_id"
            )
        return role
