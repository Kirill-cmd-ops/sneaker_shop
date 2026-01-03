from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession


async def create_record(
    session: AsyncSession,
    table_name: Callable,
    schema_create,
):
    new_record = table_name(**schema_create.dict())
    session.add(new_record)
    return new_record