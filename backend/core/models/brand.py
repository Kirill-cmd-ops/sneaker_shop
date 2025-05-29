from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.auth.models.base import Base

if TYPE_CHECKING:
    from .sneaker import Sneaker


class Brand(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)

    sneakers: Mapped[list["Sneaker"]] = relationship(back_populates="brand")
