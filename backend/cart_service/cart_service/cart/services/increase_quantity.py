from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cart_service.cart.models import db_helper, CartSneakerAssociation


async def increase_sneaker_quantity(
    cart_sneaker_id: int,
    cart_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(CartSneakerAssociation).where(
        CartSneakerAssociation.id == cart_sneaker_id,
        CartSneakerAssociation.cart_id == cart_id,
    )

    result = await session.execute(stmt)
    sneaker_record = result.scalar_one_or_none()

    if sneaker_record:
        sneaker_record.quantity += 1

        await session.commit()
        return {"status": "quantity += 1"}
    return {"status": "there is no such record"}
