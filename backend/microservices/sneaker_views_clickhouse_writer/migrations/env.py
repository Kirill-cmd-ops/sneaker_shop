from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, text
from alembic import context

from microservices.sneaker_views_clickhouse_writer.sneaker_views_clickhouse_writer.clickhouse_writer.config import settings
from microservices.sneaker_views_clickhouse_writer.sneaker_views_clickhouse_writer.clickhouse_writer.models import Base

from alembic.ddl import impl

class ClickHouseImpl(impl.DefaultImpl):
    __dialect__ = "clickhouse"
    transactional_ddl = False

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option(
    "sqlalchemy.url",
    str(settings.clickhouse_config.clickhouse_url)
)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        transactional_ddl=False,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS alembic_version (
                        version_num String
                    ) ENGINE = TinyLog
                """))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transactional_ddl=False,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
