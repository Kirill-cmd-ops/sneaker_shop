from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8009


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1/view_history"
    recent: str = "/recent"


class ApiPrefix(BaseModel):
    root: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    def build_path(self, *args: str):
        return "/" + "/".join(p.strip("/") for p in args if p)


ENV_DIR = Path(__file__).parent.parent.parent


class RedisConfig(BaseModel):
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: int


class ClickHouseConfig(BaseModel):
    clickhouse_url: str
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_secure: bool
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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(ENV_DIR / ".env.template"), str(ENV_DIR / ".env")),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    redis_config: RedisConfig
    clickhouse_config: ClickHouseConfig


settings = Settings()
