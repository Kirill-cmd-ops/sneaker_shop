from datetime import datetime

from sneaker_views_clickhouse_writer.clickhouse_writer.models import (
    db_helper,
    SneakerViewsHistory,
)


def clickhouse_insert(
    user_id: int,
    sneaker_id: int,
    sign: int,
    version: int,
    view_timestamp: datetime = None,
):
    with db_helper.session_context() as session:

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
