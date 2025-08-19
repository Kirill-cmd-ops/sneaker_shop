import re
import secrets
from typing import Optional, Union, Any


from aiokafka import AIOKafkaProducer
from fastapi import Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
    models,
)
from starlette.responses import Response

from auth_service.auth.config import settings
from auth_service.auth.dependencies.generate_refresh_token import (
    generate_refresh_token,
    encode_refresh_token,
    hash_refresh_token_add_db,
    set_value_in_cookie,
    check_refresh_token_rotation,
)
from auth_service.auth.models import User, db_helper
from auth_service.auth.schemas.user import UserCreate
from auth_service.auth.types.user_id import UserIdType

from kafka.producer import send_user_registered


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

        if not (any(c.isdigit() for c in password)):
            raise InvalidPasswordException(
                reason="The password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*]", password):
            raise InvalidPasswordException(
                reason="The password must contain at least one special character (!@#$%^&*)"
            )

        if isinstance(user, UserCreate) and user.email.lower() in password.lower():
            raise InvalidPasswordException(
                reason="The password must not contain your email."
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        producer: AIOKafkaProducer = request.app.state.kafka_producer
        await send_user_registered(producer, str(user.id))

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

    async def on_after_login(
        self,
        user: models.UP,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        refresh_token = request.cookies.get(settings.cookie.refresh_cookie_name) # None
        print("Отладка токен:", refresh_token)
        async with db_helper.session_context() as session:
            if refresh_token is None:
                user_id = None
            else:
                user_id = await check_refresh_token_rotation(session, refresh_token)
                print("Ротация результат: ", user_id)

            if user_id is None:
                user_id = getattr(user, "id", user)

                raw = secrets.token_bytes(32)
                refresh_token = generate_refresh_token(raw)
                set_value_in_cookie(
                    response,
                    value=refresh_token,
                    key=settings.cookie.refresh_cookie_name,
                    max_age=settings.cookie.refresh_cookie_max_age,
                    path=settings.cookie.cookie_path,
                    secure=settings.cookie.cookie_secure,
                    httponly=settings.cookie.cookie_httponly,
                    samesite=settings.cookie.cookie_samesite,
                )
                hash_refresh_token = encode_refresh_token(refresh_token)
                await hash_refresh_token_add_db(session, hash_refresh_token, user_id)
                print("Новый refresh токен: ", refresh_token)
            else:
                print("Используется старый refresh токен")
