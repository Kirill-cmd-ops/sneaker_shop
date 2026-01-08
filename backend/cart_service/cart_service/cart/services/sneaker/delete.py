from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import SneakerSizeAssociation, Sneaker


async def delete_sneaker(
    session: AsyncSession,
    sneaker_id: int,
):
    assoc_table = SneakerSizeAssociation
    stmt = delete(assoc_table).where(assoc_table.sneaker_id == sneaker_id)
    await session.execute(stmt)

    stmt = delete(Sneaker).where(Sneaker.id == sneaker_id)
    await session.execute(stmt)

    await session.commit()
