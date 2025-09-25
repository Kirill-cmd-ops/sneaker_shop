from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sneaker_views_clickhouse_writer.sneaker_views.config import settings
from sneaker_views_clickhouse_writer.sneaker_views.utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.clickhouse_config.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = camel_case_to_snake_case(cls.__name__)
        return f"{name}s"

    @declared_attr.directive
    def __table_args__(cls):
        return {
            'clickhouse_engine': 'MergeTree',
            'clickhouse_order_by': 'id' if hasattr(cls, 'id') else 'tuple()'
        }