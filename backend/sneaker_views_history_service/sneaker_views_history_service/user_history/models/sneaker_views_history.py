from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from sneaker_views_history_service.user_history.models import Base
from clickhouse_sqlalchemy import types as ch_types, engines


class SneakerViewsHistory(Base):
    user_id: Mapped[int] = mapped_column(ch_types.UInt32, primary_key=True)
    sneaker_id: Mapped[int] = mapped_column(ch_types.UInt32, primary_key=True)
    view_timestamp: Mapped[datetime] = mapped_column(
        ch_types.DateTime, default=datetime.utcnow
    )
    sign: Mapped[int] = mapped_column(ch_types.Int8, default=1)
    version: Mapped[int] = mapped_column(ch_types.UInt64, default=1)

    __table_args__ = (
        engines.VersionedCollapsingMergeTree(
            order_by=("user_id", "sneaker_id"),
            sign_col="sign",
            version_col="version",
        ),
    )
