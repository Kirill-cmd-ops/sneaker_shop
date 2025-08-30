from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from auth_service.auth.models import Base
from auth_service.auth.models.mixins import IntIdPkMixin

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], IntIdPkMixin, Base):
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)

