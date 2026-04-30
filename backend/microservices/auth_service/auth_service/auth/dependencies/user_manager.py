from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from microservices.auth_service.auth_service.auth.authentication.user_manager import UserManager
from microservices.auth_service.auth_service.auth.dependencies.users_db import get_users_db


async def get_user_manager(
        users_db: Annotated[
            SQLAlchemyUserDatabase,
            Depends(get_users_db),
        ],
) -> AsyncIterator[UserManager]:
    yield UserManager(users_db)
