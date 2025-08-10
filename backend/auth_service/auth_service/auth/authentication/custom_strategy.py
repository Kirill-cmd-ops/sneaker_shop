from auth_service.auth.authentication.custom_jwt import MyJWTStrategy
from auth_service.auth.config import settings


def get_jwt_strategy() -> MyJWTStrategy:
    if not settings.auth_config.jwt_private_key:
        raise ValueError("Private key not loaded! Check paths in .env")

    return MyJWTStrategy(
        secret=settings.auth_config.jwt_private_key,
        lifetime_seconds=settings.auth_config.lifetime_seconds,
        algorithm=settings.auth_config.algorithm,
        public_key=settings.auth_config.jwt_public_key,
        issuer=settings.auth_config.issuer,
        token_audience=settings.auth_config.token_audience
    )
