from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.auth.models import OAuthAccount, User, db_helper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)