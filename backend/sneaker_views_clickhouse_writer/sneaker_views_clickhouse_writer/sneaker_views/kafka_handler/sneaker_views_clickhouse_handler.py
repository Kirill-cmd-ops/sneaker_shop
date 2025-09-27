import asyncio

from sneaker_views_clickhouse_writer.sneaker_views.models import (
    db_helper,
    SneakerViewsHistory,
)


async def handle_sneaker_view_to_clickhouse(
    key: str | None,
    value: dict,
):
    user_id = value.get("user_id")
    sneaker_id = value.get("sneaker_id")

    await asyncio.get_event_loop().run_in_executor(
        None, lambda: _sync_insert(user_id, sneaker_id)
    )


def _sync_insert(user_id: int, sneaker_id: int):
    with db_helper.session_context() as session:
        sneaker_view = SneakerViewsHistory(
            user_id=user_id,
            sneaker_id=sneaker_id,
        )

        session.add(sneaker_view)
        session.commit()
