from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.auth.models import OAuthAccount, User, db_helper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_oauth_users_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(
        session=session,
        user_table=User,
        oauth_account_table=OAuthAccount,
    )
