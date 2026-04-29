from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


async def get_record_service(
        session: AsyncSession,
        table_name: Callable,
        record_id: int,
) -> DeclarativeBase | None:
    return await session.get(table_name, record_id)