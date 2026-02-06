from typing import Callable, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession


async def create_record_service(
        session: AsyncSession,
        table_name: Callable,
        data: Dict[str, Any],
):
    async with session.begin():
        new_record = table_name(**data)
        session.add(new_record)
    return new_record
