from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from sneaker_views_clickhouse_writer.sneaker_views.models.base import Base
from clickhouse_sqlalchemy import types as ch_types, engines


class SneakerViewsHistory(Base):
    id: Mapped[int] = mapped_column(ch_types.UInt64, primary_key=True)
    user_id: Mapped[int] = mapped_column(ch_types.UInt32)
    sneaker_id: Mapped[int] = mapped_column(ch_types.UInt32)
    view_timestamp: Mapped[datetime] = mapped_column(
        ch_types.DateTime, default=datetime.utcnow
    )

    __table_args__ = (
        engines.MergeTree(
            order_by=("view_timestamp",),
        ),
    )
