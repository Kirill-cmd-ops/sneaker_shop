from typing import Callable

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_record_service(
        session: AsyncSession,
        table_name: Callable,
        record_id: int,
) -> dict[str, str]:
    async with session.begin():
        delete_record_request = delete(table_name).where(table_name.id == record_id)
        await session.execute(delete_record_request)
    return {"result": "ok"}
