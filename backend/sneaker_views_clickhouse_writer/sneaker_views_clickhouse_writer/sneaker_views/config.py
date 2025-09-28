from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8008


ENV_DIR = Path(__file__).parent.parent.parent


class KafkaConfig(BaseModel):
    kafka_bootstrap_servers: str
    sneaker_viewed_topic: str
    sneaker_views_clickhouse_group: str


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


ENV_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(ENV_DIR / ".env.template"), str(ENV_DIR / ".env")),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    kafka_config: KafkaConfig
    clickhouse_config: ClickHouseConfig


settings = Settings()
