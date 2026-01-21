import asyncio

from sneaker_views_clickhouse_writer.clickhouse_writer.models import db_helper
from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.create import (
    create_user_sneaker_view_history_service,
)
from sneaker_views_clickhouse_writer.clickhouse_writer.services.sneaker_view_history.fetch import (
    get_user_sneaker_view_history_service,
)


async def create_user_sneaker_view_history_orchestrator(
    user_id: int,
    sneaker_id: int,
):
    with db_helper.session_context() as session:

        record = await get_user_sneaker_view_history_service(
            session=session,
            user_id=user_id,
            sneaker_id=sneaker_id,
        )

        if record is None:
            await asyncio.get_event_loop().run_in_executor(
                None,
                create_user_sneaker_view_history_service,
                session,
                user_id,
                sneaker_id,
                1,
                1,
                None,
            )
        else:
            record_view_timestamp = record.view_timestamp
            record_version = record.version
            record_version_next = record_version + 1

            await asyncio.get_event_loop().run_in_executor(
                None,
                create_user_sneaker_view_history_service,
                session,
                user_id,
                sneaker_id,
                -1,
                record_version_next,
                record_view_timestamp,
            )

            await asyncio.get_event_loop().run_in_executor(
                None,
                create_user_sneaker_view_history_service,
                session,
                user_id,
                sneaker_id,
                1,
                record_version_next,
                None,
            )
