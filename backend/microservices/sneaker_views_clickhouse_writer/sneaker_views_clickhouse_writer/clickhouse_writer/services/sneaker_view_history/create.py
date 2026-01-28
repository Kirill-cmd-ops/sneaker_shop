from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from microservices.sneaker_views_clickhouse_writer.sneaker_views_clickhouse_writer.clickhouse_writer.models import (
    SneakerViewsHistory,
)


def create_user_sneaker_view_history_service(
        session: AsyncSession,
        user_id: int,
        sneaker_id: int,
        sign: int,
        version: int,
        view_timestamp: datetime = None,
):
    if view_timestamp is None:
        view_timestamp = datetime.utcnow()

    try:
        sneaker_view = SneakerViewsHistory(
            user_id=user_id,
            sneaker_id=sneaker_id,
            view_timestamp=view_timestamp,
            sign=sign,
            version=version,
        )

        session.add(sneaker_view)
        session.commit()
    except Exception as e:
        print(e)
