from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.auth.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from backend.core.models import Cart


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    cart: Mapped["Cart"] = relationship(
        back_populates="user",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
