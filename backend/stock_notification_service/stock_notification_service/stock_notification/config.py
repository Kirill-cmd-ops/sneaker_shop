from pathlib import Path

from pydantic import BaseModel, computed_field
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8010


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1/subscriptions"
    one_time_prefix: str = "/v1/one_time_subscriptions"


class ApiPrefix(BaseModel):
    root: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    def build_path(self, *args: str):
        return "/" + "/".join(p.strip("/") for p in args if p)


class DatabaseConfig(BaseModel):
    use_test_db: bool = False
    url: PostgresDsn
    test_url: PostgresDsn
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

    @computed_field
    @property
    def database_url(self) -> PostgresDsn:
        return self.url if self.use_test_db == False else self.test_url


ENV_DIR = Path(__file__).parent.parent.parent
KEY_DIR = Path(__file__).parent.parent.parent.parent


class KafkaConfig(BaseModel):
    kafka_bootstrap_servers: str
    sneaker_work_topic: str
    sneaker_sizes_work_topic: str
    brand_work_topic: str
    size_work_topic: str
    user_work_topic: str
    sneaker_group_id: str
    sneaker_active_group_id: str
    sneaker_sizes_group_id: str
    brand_group_id: str
    size_group_id: str
    user_group_id: str


class RedisConfig(BaseModel):
    redis_password: str
    redis_host: str
    redis_port: int
    redis_db: int


class SMTPConfig(BaseModel):
    smtp_start_tls: bool = True
    smtp_hostname: str
    smtp_port: int
    smtp_username: str
    smtp_password: str


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
    kafka_config: KafkaConfig
    redis_config: RedisConfig
    smtp_config: SMTPConfig


settings = Settings()
