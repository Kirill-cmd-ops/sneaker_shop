import asyncio

from clickhouse_sqlalchemy import select
from sqlalchemy import desc

from sneaker_views_clickhouse_writer.clickhouse_writer.models import (
    SneakerViewsHistory,
    db_helper,
)


async def get_sneaker_view_clickhouse(
    user_id: int,
    sneaker_id: int,
):
    with db_helper.session_context() as session:

        stmt = (
            select(SneakerViewsHistory)
            .where(
                SneakerViewsHistory.user_id == user_id,
                SneakerViewsHistory.sneaker_id == sneaker_id,
                SneakerViewsHistory.sign == 1,
            )
            .order_by(desc(SneakerViewsHistory.version))
            .limit(1)
        )

        record_history = await asyncio.get_event_loop().run_in_executor(
            None, lambda: session.execute(stmt).scalar_one_or_none()
        )

    return record_history
