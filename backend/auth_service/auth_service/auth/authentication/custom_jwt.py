from fastapi_users import models
from fastapi_users.authentication import JWTStrategy
from fastapi_users.jwt import generate_jwt
from auth_service.auth.config import settings


class MyJWTStrategy(JWTStrategy):
    async def write_token(self, user: models.UP):
        data = {"sub": str(user.id), "iss": settings.auth_config.issuer, "aud": self.token_audience}
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )
