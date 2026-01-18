from typing import Annotated

from fastapi import Depends

from auth_service.auth.authentication.user_manager import UserManager

from auth_service.auth.dependencies.users_db import get_users_db


async def get_user_manager(
    users_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_users_db),
    ]
):
    yield UserManager(users_db)
