from cart_service.cart.models import db_helper
from cart_service.cart.services.cart import create_cart


async def handle_cart(key, value):
    user_id = key or value.get("id")
    async with db_helper.session_context() as session:
        await create_cart(session, user_id=int(user_id))