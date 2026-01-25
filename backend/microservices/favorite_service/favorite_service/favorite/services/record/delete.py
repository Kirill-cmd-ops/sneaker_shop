from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_service.favorite.models import db_helper


async def delete_record_service(
    table_name,
    record_id,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            delete_record_request = delete(table_name).where(table_name.id == record_id)
            await session.execute(delete_record_request)