from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi_users.models import UserProtocol
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from microservices.auth_service.auth_service.auth.models import db_helper, User


async def get_users_db(
        session: Annotated[
            "AsyncSession",
            Depends(db_helper.session_getter),
        ],
) -> AsyncGenerator[Any, Any]:
    yield User.get_db(session=session)
