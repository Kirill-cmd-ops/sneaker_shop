from pathlib import Path

from pydantic import BaseModel, Field
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from typing import Literal


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    profile: str = "/profile"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class CookieConfig(BaseModel):
    cookie_name: str = Field(default="jwt_session_cookie", pattern=r"^[a-zA-Z0-9_-]+$")
    cookie_max_age: int = Field(default=3600, ge=60)
    cookie_path: str = "/"
    cookie_secure: bool = False  # при продакшене заменить на True
    cookie_httponly: bool = True
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"


ENV_DIR = Path(__file__).parent.parent.parent


class AuthConfig(BaseModel):
    jwt_private_key_path: Path = "/app/secrets/private_key.pem"
    jwt_public_key_path: Path = "/app/secrets/public_key.pem"
    jwt_private_key: str = ""
    jwt_public_key: str = ""
    algorithm: str = "RS256"
    client_id: str = ""
    client_secret: str = ""
    state_secret: str = ""

    def model_post_init(self, __context) -> None:
        private_key_abs_path = self.jwt_private_key_path.resolve()
        if private_key_abs_path.exists():
            self.jwt_private_key = private_key_abs_path.read_text()

        public_key_abs_path = self.jwt_public_key_path.resolve()
        if public_key_abs_path.exists():
            self.jwt_public_key = public_key_abs_path.read_text()


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class KafkaConfig(BaseModel):
    kafka_bootstrap_servers: str
    registered_topic: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(ENV_DIR / ".env.template"), str(ENV_DIR / ".env")),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    cookie: CookieConfig = CookieConfig()
    auth_config: AuthConfig
    access_token: AccessToken
    kafka_config: KafkaConfig


settings = Settings()
