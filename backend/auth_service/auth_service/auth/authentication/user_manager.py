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
from auth_service.auth.kafka.producer_event.user_registered import send_user_registered

from auth_service.auth.models import User, db_helper
from auth_service.auth.refresh.dependencies.get_token_id import get_refresh_token_id
from auth_service.auth.refresh.services.add_token_in_blacklist import add_to_blacklist
from auth_service.auth.refresh.services.add_token_in_db import hash_refresh_token_add_db
from auth_service.auth.refresh.services.refresh_checks import (
    check_refresh_token_rotation,
)
from auth_service.auth.refresh.utils.encode_token import encode_refresh_token
from auth_service.auth.refresh.utils.generate_token import generate_refresh_token
from auth_service.auth.refresh.utils.set_cookie import set_value_in_cookie
from auth_service.auth.schemas import UserCreate
from auth_service.auth.services.add_role_in_db import add_role_db
from auth_service.auth.types.user_id import UserIdType

from celery_client.celery_handlers import (
    handle_request_verify,
    handle_request_reset,
    handle_after_register,
    handle_after_verify,
    handle_after_reset,
)


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
        await add_role_db(user.id, "user")

        handle_after_register.delay(
            hostname=settings.smtp_config.smtp_hostname,
            port=settings.smtp_config.smtp_port,
            start_tls=settings.smtp_config.smtp_start_tls,
            username=settings.smtp_config.smtp_username,
            password=settings.smtp_config.smtp_password,
            sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
            recipient_gmail=user.email,
            email_title="Регистрация",
            body_title=f"Благодарим за регистрацию на Sneaker Shop",
        )

    async def on_after_update(
        self,
        user: models.UP,
        update_dict: dict[str, Any],
        request: Optional[Request] = None,
    ) -> None:
        # После обновления отправялем сообщение на email для пользователя, чтобы уведомить его об изменениях профиля
        ...

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        handle_request_verify.delay(
            hostname=settings.smtp_config.smtp_hostname,
            port=settings.smtp_config.smtp_port,
            start_tls=settings.smtp_config.smtp_start_tls,
            username=settings.smtp_config.smtp_username,
            password=settings.smtp_config.smtp_password,
            sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
            recipient_gmail=user.email,
            email_title="Подтверждение почты",
            body_title=f"Перейдите по ссылке для подтверждения почты: http://localhost:8002/api/v1/auth/verify?token={token}",
        )

    async def on_after_verify(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        handle_after_verify.delay(
            hostname=settings.smtp_config.smtp_hostname,
            port=settings.smtp_config.smtp_port,
            start_tls=settings.smtp_config.smtp_start_tls,
            username=settings.smtp_config.smtp_username,
            password=settings.smtp_config.smtp_password,
            sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
            recipient_gmail=user.email,
            email_title="Подтверждение почты",
            body_title=f"Почта была успешно подтверждена",
        )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        handle_request_reset.delay(
            hostname=settings.smtp_config.smtp_hostname,
            port=settings.smtp_config.smtp_port,
            start_tls=settings.smtp_config.smtp_start_tls,
            username=settings.smtp_config.smtp_username,
            password=settings.smtp_config.smtp_password,
            sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
            recipient_gmail=user.email,
            email_title="Изменение пароля",
            body_title=f"Перейдите по ссылке для изменения пароля: http://localhost:8002/api/v1/auth/verify?token={token}&password=Qwerty2@",
        )

    async def on_after_reset_password(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        handle_after_reset.delay(
            hostname=settings.smtp_config.smtp_hostname,
            port=settings.smtp_config.smtp_port,
            start_tls=settings.smtp_config.smtp_start_tls,
            username=settings.smtp_config.smtp_username,
            password=settings.smtp_config.smtp_password,
            sender_gmail="Sneaker Shop <bondarenkokirill150208@gmail.com>",
            recipient_gmail=user.email,
            email_title="Изменение пароля",
            body_title="Пароль был успешно изменен",
        )

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
        refresh_token = request.cookies.get(settings.cookie.refresh_cookie_name)
        print("Отладка токен:", refresh_token)
        async with db_helper.session_context() as session:
            if refresh_token is None:
                user_id = None
            else:
                user_id = await check_refresh_token_rotation(session, refresh_token)
                print("Ротация результат: ", user_id)

            if user_id is None:
                if refresh_token:
                    hash_refresh_token = encode_refresh_token(refresh_token)
                    print("Хеш токена: ", hash_refresh_token)
                    id_refresh_token = await get_refresh_token_id(
                        hash_refresh_token, session
                    )
                    await add_to_blacklist(session, id_refresh_token)
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
