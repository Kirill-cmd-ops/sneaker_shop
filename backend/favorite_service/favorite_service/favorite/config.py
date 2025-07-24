from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    favorite: str = "/favorite"
    favorite_sneaker: str = "/favorite_sneaker"


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


ENV_DIR = Path(__file__).parent.parent.parent
KEY_DIR = Path(__file__).parent.parent.parent.parent


class AuthConfig(BaseModel):
    jwt_private_key_path: Path = KEY_DIR / "secrets" / "private_key.pem"
    jwt_private_key: str = ""
    algorithm: str = "RS256"

    def model_post_init(self, __context) -> None:
        private_key_abs_path = self.jwt_private_key_path.resolve()
        if private_key_abs_path.exists():
            self.jwt_private_key = private_key_abs_path.read_text()


class KafkaConfig(BaseModel):
    kafka_bootstrap_servers: str
    registered_topic: str
    favorite_group_id: str


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
    auth_config: AuthConfig
    kafka_config: KafkaConfig


settings = Settings()
