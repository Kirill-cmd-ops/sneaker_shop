import re
from typing import Optional, Union

from fastapi import Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
)

from core.models import User
from core.config import settings
from core.schemas.user import UserCreate
from core.types.user_id import UserIdType


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    # async def validate_password(
    #     self,
    #     password: str,
    #     user: Union[UserCreate, User],
    # ) -> None:
    #     if len(password) < 8:
    #         raise InvalidPasswordException(
    #             reason="Password less than 8 characters",
    #         )
    #
    #     if not (
    #         any(c.islower() for c in password) and any(c.isupper() for c in password)
    #     ):
    #         raise InvalidPasswordException(
    #             reason="The password must contain at least one uppercase and one lowercase letter."
    #         )
    #
    #     if not (
    #             any(c.isdigit() for c in password)
    #     ):
    #         raise InvalidPasswordException(
    #             reason="The password must contain at least one digit."
    #         )
    #
    #     if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>/?]', password):
    #         raise InvalidPasswordException(
    #             reason="The password must contain at least one special character (!@#$%^&*)"
    #         )
    #
    #     if isinstance(user, UserCreate) and user.email.lower() in password.lower():
    #         raise InvalidPasswordException(
    #             reason="The password must not contain your email."
    #         )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
