from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.auth.authentication.fastapi_users import fastapi_users
from backend.auth.models import User
from backend.auth.models import db_helper
from backend.core.schemas.cart_sneaker import CartSneakerUpdate, CartSneakerCreate
from backend.core.services.cart_sneaker import (
    create_sneaker_to_cart,
    update_sneaker_to_cart,
    delete_sneaker_to_cart,
)
from backend.core.models import Cart

router = APIRouter()


@router.post("/", response_model=dict)
async def call_create_sneaker_to_cart(
    item: CartSneakerCreate,
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = select(Cart).filter(Cart.user_id == user.id)
    result = await session.execute(stmt)
    user_cart = result.scalar_one_or_none()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Корзина пользователя не найдена")

    new_item = await create_sneaker_to_cart(
        session,
        cart_id=user_cart.id,
        sneaker_id=item.sneaker_id,
        sneaker_size=item.sneaker_size,
    )
    return {"status": "Элемент добавлен", "item_id": new_item.id}


@router.put("/{association_id}", response_model=dict)
async def call_update_sneaker_to_cart(
    association_id: int,
    item_data: CartSneakerUpdate,
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    updated_item = await update_sneaker_to_cart(
        session, association_id=association_id, sneaker_size=item_data.sneaker_size
    )
    return {"status": "Элемент обновлён", "item_id": updated_item.id}


@router.delete("/{association_id}", response_model=dict)
async def call_delete_sneaker_to_cart(
    association_id: int,
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    await delete_sneaker_to_cart(session, association_id=association_id)
    return {"status": "Элемент удалён"}
