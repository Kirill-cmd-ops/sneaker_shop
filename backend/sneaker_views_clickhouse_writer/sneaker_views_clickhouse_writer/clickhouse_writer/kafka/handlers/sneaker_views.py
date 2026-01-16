import asyncio

from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.create import (
    create_user_sneaker_view_history_service,
)
from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)


async def handle_sneaker_viewed_event(
    key: str | None,
    value: dict,
):
    try:
        user_id = value.get("user_id")
        sneaker_id = value.get("sneaker_id")

        record = await get_user_sneaker_view_history_service(
            user_id=user_id, sneaker_id=sneaker_id
        )

        if record is None:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: create_user_sneaker_view_history_service(
                    user_id=user_id,
                    sneaker_id=sneaker_id,
                    sign=1,
                    version=1,
                ),
            )
        else:
            record_view_timestamp = record.view_timestamp
            record_version = record.version
            record_version_next = record_version + 1

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: create_user_sneaker_view_history_service(
                    user_id=user_id,
                    sneaker_id=sneaker_id,
                    sign=-1,
                    version=record_version_next,
                    view_timestamp=record_view_timestamp,
                ),
            )

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: create_user_sneaker_view_history_service(
                    user_id=user_id,
                    sneaker_id=sneaker_id,
                    sign=1,
                    version=record_version_next,
                ),
            )
    except Exception as e:
        print(e)
