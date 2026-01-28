from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from microservices.auth_service.auth_service.auth.models import Base
from microservices.auth_service.auth_service.auth.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .role_permission import RolePermissionAssociation
    from .role import Role


class Permission(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    role_association: Mapped[list["RolePermissionAssociation"]] = relationship(
        "RolePermissionAssociation", back_populates="permission"
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary="role_permission_associations",
        viewonly=True,
    )
