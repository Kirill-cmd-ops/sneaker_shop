from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession


async def create_record_service(
    session: AsyncSession,
    table_name: Callable,
    schema_create,
):
    new_record = table_name(**schema_create.dict())
    session.add(new_record)
    await session.commit()
    return new_record