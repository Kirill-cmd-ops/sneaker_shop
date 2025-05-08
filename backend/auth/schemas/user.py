from typing import Optional

from fastapi_users import schemas

from backend.auth.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
