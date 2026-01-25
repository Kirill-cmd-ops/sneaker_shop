from sneaker_views_history_service.user_history.config import settings

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: Engine = create_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def dispose(self) -> None:
        self.engine.dispose()

    def session_getter(self) -> Generator[Session, None, None]:
        with self.session_factory() as session:
            yield session

    @contextmanager
    def session_context(self) -> Generator[Session, None, None]:
        with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.clickhouse_config.clickhouse_url),
    echo=settings.clickhouse_config.echo,
    echo_pool=settings.clickhouse_config.echo_pool,
    pool_size=settings.clickhouse_config.pool_size,
    max_overflow=settings.clickhouse_config.max_overflow,
)
