from typing import Optional

from fastapi import HTTPException
from fastapi_users import schemas
from pydantic import field_validator

from auth_service.auth.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateWithoutConfirm(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserCreate(UserCreateWithoutConfirm):
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def check_passwords(cls, confirm_password, user_model):
        password = user_model.data.get("password")
        if password and confirm_password != password:
            raise HTTPException(status_code=422, detail="Пароли не совпадают")
        return confirm_password


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
