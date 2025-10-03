import asyncio

from sqlalchemy import select, text, desc
from sqlalchemy.orm import Session

from sneaker_views_history_service.user_history.models import SneakerViewsHistory


async def get_sneaker_views_clickhouse(
    session: Session,
    user_id: int,
    limit: int | None = None,
):
    stmt = (
        select(SneakerViewsHistory)
        .where(
            SneakerViewsHistory.user_id == user_id,
            SneakerViewsHistory.sign == 1,
            )
        .order_by(
            SneakerViewsHistory.sneaker_id,
            desc(SneakerViewsHistory.version),
        )
        .distinct(SneakerViewsHistory.sneaker_id)
    )
    if limit is not None:
        stmt = stmt.limit(30)


    records_history = await asyncio.get_event_loop().run_in_executor(
        None, lambda: session.execute(stmt).scalars().all()
    )

    return records_history
