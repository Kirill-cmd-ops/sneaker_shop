from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from auth_service.auth.models import Base
from auth_service.auth.models.mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .role_permission import RolePermissionAssociation
    from .user_role import UserRoleAssociation
    from .permission import Permission
    from .user import User


class Role(Base, IntIdPkMixin):
    name: Mapped[str]

    permission_association: Mapped[list["RolePermissionAssociation"]] = relationship(
        "RolePermissionAssociation",
        back_populates="role",
    )

    user_association: Mapped[list["UserRoleAssociation"]] = relationship(
        "UserRoleAssociation",
        back_populates="role",
    )

    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permission_associations",
        viewonly=True
    )

    users: Mapped[list["User"]] = relationship(
        secondary="user_role_associations",
        viewonly=True
    )
