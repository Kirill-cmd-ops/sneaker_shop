from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from auth_service.auth.models.base import Base
from auth_service.auth.models.mixins import IntIdPkMixin


class RefreshToken(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(
        nullable=False,
    )
    issued_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
    )
    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )
    revoked: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )
