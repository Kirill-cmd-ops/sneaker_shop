from sqlalchemy import delete

from catalog_service.catalog.models import SneakerSizeAssociation, Sneaker, db_helper


async def delete_sneaker_service(
    sneaker_id: int,
):
    async with db_helper.session_context() as session:
        async with session.begin():
            assoc_table = SneakerSizeAssociation
            stmt = delete(assoc_table).where(assoc_table.sneaker_id == sneaker_id)
            await session.execute(stmt)

            stmt = delete(Sneaker).where(Sneaker.id == sneaker_id)
            await session.execute(stmt)
