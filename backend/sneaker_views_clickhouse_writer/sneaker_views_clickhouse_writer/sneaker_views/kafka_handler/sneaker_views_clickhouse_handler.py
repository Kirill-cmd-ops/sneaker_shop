from sneaker_views_clickhouse_writer.sneaker_views.models.db_helper import db_helper
from sneaker_views_clickhouse_writer.sneaker_views.models.sneaker_views_history import (
    SneakerViewsHistory,
)


async def handle_sneaker_view_to_clickhouse(
    key: str | None,
    value: dict,
):
    with db_helper.session_context() as session:
        user_id = value.get("user_id")
        sneaker_id = value.get("sneaker_id")

        sneaker_view = SneakerViewsHistory(
            user_id=user_id,
            sneaker_id=sneaker_id,
        )

        session.add(sneaker_view)
        session.commit()
