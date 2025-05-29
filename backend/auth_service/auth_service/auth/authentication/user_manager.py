import re
from typing import Optional, Union, Any

from fastapi import Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException, models,
)

from auth_service.auth.config import settings
from auth_service.auth.models import User
from auth_service.auth.schemas.user import UserCreate
from auth_service.auth.types.user_id import UserIdType


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password less than 8 characters",
            )

        if not (
            any(c.islower() for c in password) and any(c.isupper() for c in password)
        ):
            raise InvalidPasswordException(
                reason="The password must contain at least one uppercase and one lowercase letter."
            )

        if not (
                any(c.isdigit() for c in password)
        ):
            raise InvalidPasswordException(
                reason="The password must contain at least one digit."
            )

        if not re.search(r'[!@#$%^&*]', password):
            raise InvalidPasswordException(
                reason="The password must contain at least one special character (!@#$%^&*)"
            )

        if isinstance(user, UserCreate) and user.email.lower() in password.lower():
            raise InvalidPasswordException(
                reason="The password must not contain your email."
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # После регистрации отправялем сообщение на email для активации аккаунта
        ...

    async def on_after_update(
        self,
        user: models.UP,
        update_dict: dict[str, Any],
        request: Optional[Request] = None,
    ) -> None:
        # После обновления отправялем сообщение на email для пользователя, чтобы уведомить его об изменениях профиля
        ...

    async def on_after_verify(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        # После активации аккаунта, будем отправлять письмо на почту, уведомляя об этом пользователя
        ...

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # После запроса отправляем на email сообщенрие с ссылкой на восстановление пароля
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # После запроса на подтвеждение логина, мы будем отправлять сообщение на email
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_before_delete(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        # отправка подтверждающего письма на почту пользователя
        ...
