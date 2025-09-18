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
    sneaker_views_redis_group: str


class RedisConfig(BaseModel):
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(ENV_DIR / ".env.template"), str(ENV_DIR / ".env")),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    kafka_config: KafkaConfig
    redis_config: RedisConfig


settings = Settings()
