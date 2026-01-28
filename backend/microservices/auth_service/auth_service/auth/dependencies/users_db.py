from typing import Annotated

from fastapi import Depends

from microservices.auth_service.auth_service.auth.models import db_helper, User


async def get_users_db(
        session: Annotated[
            "AsyncSession",
            Depends(db_helper.session_getter),
        ],
):
    yield User.get_db(session=session)
