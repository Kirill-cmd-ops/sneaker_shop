from fastapi import HTTPException
from sqlalchemy import select

from auth_service.auth.models import db_helper, User, Role, UserRoleAssociation


async def add_role_db(user_id: int, role_name: str):
    async with db_helper.session_context() as session:
        user_object = await session.get(User, user_id)
        if not user_object:
            raise HTTPException(status_code=404, detail="Данного пользователя нету в бд")

        stmt = select(Role.id).where(Role.name == role_name)
        result = await session.execute(stmt)
        role_id = result.scalar_one_or_none()
        if not role_id:
            raise HTTPException(status_code=404, detail="Данная роль отсутствует в бд")

        user_role_association = UserRoleAssociation(user_id=user_id, role_id=role_id)
        session.add(user_role_association)
        await session.commit()
