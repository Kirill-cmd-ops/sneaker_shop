from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sneaker_views_history_service.user_history.config import settings
from sneaker_views_history_service.user_history.utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.clickhouse_config.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = camel_case_to_snake_case(cls.__name__)
        if name.endswith("y"):
            return f"{name[:-1]}ies"
        return f"{name}s"

    @declared_attr.directive
    def __table_args__(cls):
        return {
            "clickhouse_engine": "MergeTree",
            "clickhouse_order_by": "id" if hasattr(cls, "id") else "tuple()",
        }
