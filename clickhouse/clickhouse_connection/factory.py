from clickhouse_driver import Client


def get_clickhouse_factory(
    user: str,
    password: str,
    host: str = "clickhouse",
    port: int = 9000,
    secure: bool = False,
):
    async def get_clickhouse():
        clickhouse_client = Client(
            host=host,
            port=port,
            user=user,
            password=password,
            secure=secure,
        )
        try:
            yield clickhouse_client
        finally:
            clickhouse_client.disconnect()

    return get_clickhouse
