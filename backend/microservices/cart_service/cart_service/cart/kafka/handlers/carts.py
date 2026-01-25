from cart_service.cart.models import db_helper
from cart_service.cart.services.cart.create import create_cart_service


async def handle_cart_event(key, value):
    user_id = key or value.get("id")
    await create_cart_service(user_id=int(user_id))
