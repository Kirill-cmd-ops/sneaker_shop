from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8007


ENV_DIR = Path(__file__).parent.parent.parent


class KafkaConfig(BaseModel):
    kafka_bootstrap_servers: str
    sneaker_viewed_topic: str
    sneaker_views_clickhouse_group: str


class ClickHouseConfig(BaseModel):
    clickhouse_user: str
    clickhouse_password: str
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_secure: bool


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
