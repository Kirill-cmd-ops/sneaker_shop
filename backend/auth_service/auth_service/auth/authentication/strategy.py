from fastapi_users.authentication import JWTStrategy
from auth_service.auth.config import settings


def get_jwt_strategy() -> JWTStrategy:
    if not settings.auth_config.jwt_private_key:
        raise ValueError("Private key not loaded! Check paths in .env")

    return JWTStrategy(
        secret=settings.auth_config.jwt_private_key,
        lifetime_seconds=settings.auth_config.lifetime_seconds,
        algorithm=settings.auth_config.algorithm,
        public_key=settings.auth_config.jwt_public_key,
    )
