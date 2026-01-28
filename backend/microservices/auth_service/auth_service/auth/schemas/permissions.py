from pydantic import BaseModel


class UpdatePermissions(BaseModel):
    list_permission: list[int]
