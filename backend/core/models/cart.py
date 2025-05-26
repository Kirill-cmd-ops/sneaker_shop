from sqlalchemy import ForeignKey
from backend.auth.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.auth.models import User


class Cart(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)

    user: Mapped["User"] = relationship(
        back_populates="cart",
    )
