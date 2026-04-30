from pydantic import BaseModel, Field


class UpdatePermissions(BaseModel):
    list_permission: list[int]


class RolePermissionsResponse(BaseModel):
    permissions: list[str]
