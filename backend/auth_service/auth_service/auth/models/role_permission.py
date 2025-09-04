from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth_service.auth.models import Base
from auth_service.auth.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .role import Role
    from .permission import Permission


class RolePermissionAssociation(IntIdPkMixin, Base):
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="permission_association",
    )
    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="role_association",
    )

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
