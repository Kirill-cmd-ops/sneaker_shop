from datetime import datetime

from clickhouse.clickhouse_connection.factory import get_clickhouse_factory
from sneaker_views_clickhouse_writer.sneaker_views.config import settings

clickhouse_factory = get_clickhouse_factory(
    user=settings.clickhouse_config.clickhouse_user,
    password=settings.clickhouse_config.clickhouse_password,
    host=settings.clickhouse_config.clickhouse_host,
    port=settings.clickhouse_config.clickhouse_port,
    secure=settings.clickhouse_config.clickhouse_secure,
)


async def handle_sneaker_view_to_clickhouse(
    key: str | None,
    value: dict,
):
    async for clickhouse_client in clickhouse_factory():
        user_id = value.get("user_id")
        sneaker_id = value.get("sneaker_id")

        clickhouse_client.execute(
            "INSERT INTO sneaker_views_db.sneaker_views_history VALUES",
            [{
                "user_id": user_id,
                "sneaker_id": sneaker_id,
                "view_timestamp": datetime.now()
            }]
        )
