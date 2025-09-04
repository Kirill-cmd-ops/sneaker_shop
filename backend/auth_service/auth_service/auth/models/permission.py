from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from auth_service.auth.models import Base
from auth_service.auth.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .role_permission import RolePermissionAssociation
    from .role import Role

class Permission(IntIdPkMixin, Base):
    name: Mapped[str]

    role_association: Mapped[list["RolePermissionAssociation"]] = relationship(
        "RolePermissionAssociation",
        back_populates="permission"
    )

    roles: Mapped[list["Role"]] = relationship(
        secondary="role_permission_association",
        viewonly=True
    )
