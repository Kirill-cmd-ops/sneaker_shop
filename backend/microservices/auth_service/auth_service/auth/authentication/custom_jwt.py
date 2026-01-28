from typing import Optional

from fastapi_users import models
from fastapi_users.authentication import JWTStrategy
from fastapi_users.jwt import generate_jwt, SecretType

from microservices.auth_service.auth_service.auth.services.user_role.fetch import get_user_role


class MyJWTStrategy(JWTStrategy):
    def __init__(
            self,
            secret: SecretType,
            issuer: str,
            lifetime_seconds: Optional[int],
            token_audience: list[str],
            allowed_audience: list[str],
            algorithm: str = "RS256",
            public_key: Optional[SecretType] = None,
    ):
        super().__init__(
            secret=secret,
            lifetime_seconds=lifetime_seconds,
            token_audience=token_audience,
            algorithm=algorithm,
            public_key=public_key,
        )
        self.issuer = issuer
        self.allowed_audience = allowed_audience

    async def write_token(self, user: models.UP):
        if not set(self.token_audience).issubset(self.allowed_audience):
            raise ValueError(
                "Значение aud некорректно для access токена, который вы пытаетесь создать"
            )

        sub = getattr(user, "id", user)
        role = await get_user_role(user_id=sub)

        data = {
            "sub": str(sub),
            "iss": self.issuer,
            "aud": self.token_audience,
            "user_role": role,
        }
        return generate_jwt(
            data=data,
            secret=self.encode_key,
            lifetime_seconds=self.lifetime_seconds,
            algorithm=self.algorithm,
        )
