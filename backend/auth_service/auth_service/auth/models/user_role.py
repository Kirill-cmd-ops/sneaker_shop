from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.auth.models import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .role import Role
    from .user import User


class UserRoleAssociation(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), index=True)

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_association",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="role_association",
    )
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)
