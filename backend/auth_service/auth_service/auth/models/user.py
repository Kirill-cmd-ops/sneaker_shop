from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.auth.types.user_id import UserIdType

from auth_service.auth.models.oauth_account import OAuthAccount
from auth_service.auth.models.base import Base
from auth_service.auth.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .user_role import UserRoleAssociation
    from .role import Role

class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)

    oauth_accounts = relationship("OAuthAccount", lazy="joined")

    role_association: Mapped[list["UserRoleAssociation"]] = relationship(
        "UserRoleAssociation",
        back_populates="user",
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary="user_role_associations",
        viewonly=True
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls, OAuthAccount)
