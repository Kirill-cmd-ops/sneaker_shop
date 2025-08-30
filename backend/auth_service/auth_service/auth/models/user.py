from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.auth.types.user_id import UserIdType

from auth_service.auth.models.oauth_account import OAuthAccount
from auth_service.auth.models.base import Base
from auth_service.auth.models.mixins import IntIdPkMixin


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    oauth_accounts = relationship("OAuthAccount", lazy="joined")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls, OAuthAccount)
