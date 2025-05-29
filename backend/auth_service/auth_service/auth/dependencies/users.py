from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends

from backend.auth_service.auth_service.auth.models import db_helper, User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield User.get_db(session=session)
