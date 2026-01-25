import asyncio

from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.create import (
    create_user_sneaker_view_history_service,
)
from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)
from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.orchestrators import (
    create_user_sneaker_view_history_orchestrator,
)


async def handle_sneaker_viewed_event(
    key: str | None,
    value: dict,
):
    try:
        user_id = value.get("user_id")
        sneaker_id = value.get("sneaker_id")

        await create_user_sneaker_view_history_orchestrator(
            user_id=user_id,
            sneaker_id=sneaker_id,
        )
    except Exception as e:
        print(e)
