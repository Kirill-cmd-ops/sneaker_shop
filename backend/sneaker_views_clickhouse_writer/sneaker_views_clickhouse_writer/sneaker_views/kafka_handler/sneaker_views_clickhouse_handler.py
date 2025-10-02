import asyncio

from sqlalchemy.orm import Session

from sneaker_views_clickhouse_writer.sneaker_views.services.add_data_clickhouse import (
    clickhouse_insert,
)
from sneaker_views_clickhouse_writer.sneaker_views.services.get_view_clickhouse import (
    get_sneaker_view_clickhouse,
)


async def handle_sneaker_view_to_clickhouse(
    key: str | None,
    value: dict,
):
    try:
        user_id = value.get("user_id")
        sneaker_id = value.get("sneaker_id")

        record = await get_sneaker_view_clickhouse(user_id, sneaker_id)

        if record is None:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: clickhouse_insert(
                    user_id=user_id, sneaker_id=sneaker_id, sign=1, version=1
                ),
            )
        else:
            record_view_timestamp = record.view_timestamp
            record_version = record.version
            record_version_next = record_version + 1

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: clickhouse_insert(
                    user_id=user_id,
                    sneaker_id=sneaker_id,
                    sign=-1,
                    version=record_version_next,
                    view_timestamp=record_view_timestamp,
                ),
            )

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: clickhouse_insert(
                    user_id=user_id,
                    sneaker_id=sneaker_id,
                    sign=1,
                    version=record_version_next,
                ),
            )
    except Exception as e:
        print(e)
