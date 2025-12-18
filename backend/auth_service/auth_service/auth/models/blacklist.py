from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from auth_service.auth.models.base import Base
from auth_service.auth.models.mixins import IntIdPkMixin


class Blacklist(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint("refresh_token_id"),
    )
    refresh_token_id: Mapped[int] = mapped_column(ForeignKey("refresh_tokens.id", ondelete="CASCADE"), nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    revoked_reason: Mapped[str] = mapped_column(nullable=False, default="The token has been replaced with a new one")
