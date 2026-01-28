from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from microservices.auth_service.auth_service.auth.models.base import Base
from microservices.auth_service.auth_service.auth.models.mixins import IntIdPkMixin

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base, IntIdPkMixin):
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )
