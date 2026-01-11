from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_record_service(
        session: AsyncSession,
        table_name,
        record_id,
):
    delete_record_request = delete(table_name).where(table_name.id == record_id)
    await session.execute(delete_record_request)
    await session.commit()
    return {"result": "ok"}