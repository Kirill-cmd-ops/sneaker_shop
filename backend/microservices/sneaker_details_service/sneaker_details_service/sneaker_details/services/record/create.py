from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession


async def create_record_service(
    session: AsyncSession,
    table_name: Callable,
    schema_create,
):
    async with session.begin():
        new_record = table_name(**schema_create.dict())
        session.add(new_record)
    return new_record
