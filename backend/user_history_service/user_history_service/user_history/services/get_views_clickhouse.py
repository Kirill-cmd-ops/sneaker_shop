from sqlalchemy import select
from sqlalchemy.orm import Session

from user_history_service.user_history.models import SneakerViewsHistory


# TODO: Переписать на более оптимальный вариант, используй скользящие окна, группировка или что-то иное
async def get_sneaker_views_clickhouse(
    session: Session,
    user_id: int,
):
    """
    Функция занимается получением данных из ClickHouse
    :param session: Синхронная сессия, которая обеспечивает связь с ClickHouse
    :param user_id: Идентификатор пользователя
    :return: Список обьектов, либо пустой список, если обьекты не найдены
    """
    stmt = (
        select(SneakerViewsHistory)
        .where(SneakerViewsHistory.user_id == user_id)
        .order_by(SneakerViewsHistory.view_timestamp.desc())
        .limit(40)
    )
    result = session.execute(stmt).unique()
    records_history = result.scalars().all()
    print("Часть где работает онли ClickHouse: ", records_history)

    return records_history
