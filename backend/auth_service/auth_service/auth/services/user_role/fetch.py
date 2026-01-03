from fastapi import HTTPException
from sqlalchemy import select

from auth_service.auth.models import db_helper, Role, UserRoleAssociation


async def get_user_role(user_id: int):
    async with db_helper.session_context() as session:
        stmt = (
            select(Role.name)
            .join(UserRoleAssociation, Role.id == UserRoleAssociation.role_id)
            .where(UserRoleAssociation.user_id == user_id)
        )
        result = await session.execute(stmt)
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(
                status_code=404, detail="У данного пользователя нету role_id"
            )
        return role
