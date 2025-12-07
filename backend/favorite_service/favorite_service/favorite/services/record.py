from collections.abc import Callable

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


async def create_record(
    session: AsyncSession,
    table_name: Callable,
    schema_create,
):
    new_record = table_name(**schema_create.dict())
    session.add(new_record)
    await session.commit()
    return new_record


async def delete_record(
        session: AsyncSession,
        table_name,
        record_id,
):
    delete_record_request = delete(table_name).where(table_name.id == record_id)
    await session.execute(delete_record_request)
    await session.commit()
    return {"result": "ok"}
